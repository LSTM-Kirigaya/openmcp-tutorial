from typing import List, Dict, Optional, Union
from enum import Enum
from pathlib import Path
import asyncio
import os
import subprocess
import shutil

from mcp.server.fastmcp import FastMCP
from pyppeteer import launch
from pydantic import BaseModel

from graph import export_to_relation_graph

current_file_path = Path(__file__).resolve()
current_dir_path = current_file_path.parent
report_dir = current_dir_path / "report"

def build_report():
    """
    在 report_dir 这个项目中执行 npm run build
    并使用无头浏览器将生成的 html 转换成 pdf
    """
    node_model_path = report_dir / "node_modules"
    if not node_model_path.exists():
        subprocess.run(["npm", "i"], cwd=report_dir, capture_output=True)
    
    dist_path = report_dir / "dist"

    if dist_path.exists():
        # 删除 dist 文件夹
        shutil.rmtree(dist_path)

    subprocess.run(["npm", "run", "build"], cwd=report_dir, capture_output=True)

    if dist_path.exists():
        print('build success')
        html = dist_path / "index.html"
        return html
    else:
        print('build failed')
    return None
async def html_to_pdf(html_path: str, output_path: str):
    browser = await launch(headless=True,
                           args=['--no-sandbox', '--disable-setuid-sandbox'])
    page = await browser.newPage()

    # 加载本地 HTML 文件
    html_abs_path = f'file://{os.path.abspath(html_path)}'
    await page.goto(html_abs_path, {'waitUntil': 'networkidle0'})

    # 导出 PDF，参数符合需求
    await page.pdf({
        'path': output_path,
        'format': 'A4',
        'printBackground': True,   # 保留背景图片和颜色
        'margin': {
            'top': '0mm',
            'right': '0mm',
            'bottom': '0mm',
            'left': '0mm'
        },
        'scale': 1.0 
    })

    await browser.close()

# 初始化 MCP Server
mcp = FastMCP("ChatSummaryServer", version="1.0.0")

class SummaryTopic(BaseModel):
    topic: str
    contributors: List[str]
    detail: str

class SummarizeChatParams(BaseModel):
    groupId: str
    messages: List[SummaryTopic]

class UserTitle(str, Enum):
    WATER_TALKER = "水群小能手"
    TECH_EXPERT = "技术专家"
    NIGHT_OWL = "夜猫子"
    EMOJI_MASTER = "表情包批发商"
    KOL = "KOL"

class SummarizeUserTitle(BaseModel):
    name: str
    qq: int
    title: str
    mbti: str

class SummarizeUserParams(BaseModel):
    groupId: str
    titles: List[SummarizeUserTitle]


class SummaryStatisticParams(BaseModel):
    message_count: int
    total_characters: int
    participant_count: int
    most_active_period: str

@mcp.prompt()
def lead_summary() -> str:
    return """
你是一个帮我进行群聊信息总结的助手，你的名字是 TIP，你现在需要根据用户输入的 json 来自动总结该群一天的表现，json 是一个从群聊中提取出来的数据包，里面有群聊内容和群聊的基本信息。

生成总结内容时，你需要严格遵守下面的几个准则：
- 对于比较有价值的点，稍微用一两句话详细讲讲，比如不要生成 “锦恢和元可可简单讨论了Trae 对 MCP 的具体支持情况”，而是生成更加具体的讨论内容，让其他人只看这个消息就能知道讨论中有价值的，有营养的信息。
- 对于其中的部分信息，你需要特意提到主题施加的主体是谁，是哪个群友做了什么事情，而不要直接生成和群友没有关系的语句。
- 对于每一条总结，尽量讲清楚前因后果，以及话题的结论，是什么，为什么，怎么做，如果用户没有讲到细节，则可以不用这么做。

群聊消息的一个例子如下：

```json
{
    "sender": "元可可YoCoco",
    "time": "00:14",
    "content": "GitHub像素头像生成算法吗？",
    "replyName": "@锦恢",
    "replyText": "顾佬，你之前说的那个随机头像的项目是什么来着"
}
```

- sender: 群友名称
- time: 群友发言的时间
- content: 群友发言的内容
- replyName(可能没有): 群友回复的群友名称
- replyText(可能没有): 群友回复的群友发言的内容

你必须主动地调用 summarize_chat, summarize_user 和 summary_statistic 这三个方法至少一次来返回总结的内容。

调用 summarize_chat 时，你只需要挑选小于等于八位群友进行称号赋予就行，每一个群友最多一个称号，每个称号只能赋给一个人。这一步类似 CSGO 的结算动画中给每一个小队成员的称号赋予。
，可选的称号有如下的几个：

- 水群小能手: 进行发言，而且大部分都和技术没有关系的人
- 技术专家: 贡献技术相关的话题的人，且主导了对话内容
- 夜猫子: 经常在凌晨发言的人
- 沉默终结者：经常开启话题的人
- 表情包批发商: 经常发图片的人
- KOL: 在某一个话题非常有发言权的关键人物
- 剧作家：平均发言长度最长的人
- ... (你可以自行进行拓展添加)

当 summarize_chat, summarize_user 和 summary_statistic 都被调用后，则调用 export_everything 导出结果

使用 export_everything 函数的时候，导出的名字必须是类似 群聊总结.{年}.{月}.{日} 的格式, 比如 export_everything("群聊总结.2025.08.03")

接下来是用户的群聊数据 json：

"""

@mcp.tool()
def summarize_chat(params: SummarizeChatParams):
    """对一段群聊消息进行总结，输出统计"""
    data = params.model_dump_json(indent=2)
    json_path = (report_dir / "src" / "summarize_chat.json").as_posix()
    with open(json_path, "w") as f:
        f.write(data)

    return 'write to ' + json_path

@mcp.tool()
def summarize_user(params: SummarizeUserParams):
    """总结群友的聊天表现和各自成就称号和 MBTI 表现"""
    data = params.model_dump_json(indent=2)
    json_path = (report_dir / "src" / "summarize_user.json").as_posix()
    with open(json_path, "w") as f:
        f.write(data)

    return 'write to ' + json_path

@mcp.tool()
async def export_everything(file_name: str):
    """将信息导出为 pdf"""
    html = build_report()

    pdf_home = Path('summary_pdf')
    relation_image_home = Path('summary_image')

    if not pdf_home.exists():
        pdf_home.mkdir(parents=True)

    if not relation_image_home.exists():
        relation_image_home.mkdir(parents=True)

    # 转为绝对路径
    pdf_path = (pdf_home / Path(file_name + '.pdf')).resolve()
    image_path = (relation_image_home / Path(file_name + '.png')).resolve()

    if html is not None:
        await html_to_pdf(html, str(pdf_path))
        export_to_relation_graph(image_path)

        return str(pdf_path), str(image_path)
    else:
        return None


@mcp.tool()
def summary_statistic(params: SummaryStatisticParams):
    """提供群聊的基本统计信息"""
    data = params.model_dump_json(indent=2)
    json_path = (report_dir / "src" / "summary_statistic.json").as_posix()
    with open(json_path, "w") as f:
        f.write(data)
    
    return 'write to ' + json_path