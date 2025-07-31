from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union
from datetime import datetime
from enum import Enum

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
    title: str

class SummarizeUserParams(BaseModel):
    groupId: str
    titles: List[SummarizeUserTitle]

def default_achievements() -> List[Dict]:
    return [
        {
            "id": "water_talker",
            "title": "水群小能手",
            "description": "在聊天中发言最多的人",
            "criteria": "消息数排名第一",
            "awardedTo": []
        },
        {
            "id": "tech_expert",
            "title": "技术专家",
            "description": "在技术话题中贡献最多的人",
            "criteria": "参与超过 5 个技术相关话题",
            "awardedTo": []
        },
        {
            "id": "night_owl",
            "title": "深夜键盘侠",
            "description": "在凌晨时间段依旧活跃的人",
            "criteria": "凌晨 0:00-4:00 发言超过 10 条",
            "awardedTo": []
        },
        {
            "id": "emoji_master",
            "title": "表情帝",
            "description": "最爱用表情包的人",
            "criteria": "超过 30% 消息包含表情",
            "awardedTo": []
        }
    ]


@mcp.prompt()
def lead_summary() -> str:
    return """
你是一个帮我进行群聊信息总结的助手，你的名字是 TIP，你现在需要根据用户输入的 json 来自动总结该群一天的表现，json 是一个从群聊中提取出来的数据包，里面有群聊内容和群聊的基本信息。

生成总结内容时，你需要严格遵守下面的几个准则：
- 对于比较有价值的点，稍微用一两句话详细讲讲，比如不要生成 “锦恢和元可可简单讨论了Trae 对 MCP 的具体支持情况”，而是生成更加具体的讨论内容，让其他人只看这个消息就能知道讨论中有价值的，有营养的信息。
- 对于其中的部分信息，你需要特意提到主题施加的主体是谁，是哪个群友做了什么事情，而不要直接生成和群友没有关系的语句。

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

你必须主动地调用 summarize_chat 和 summarize_user 这两个方法至少一次来返回总结的内容。

调用 summarize_chat 时，你只需要挑选小于五位群友进行称号赋予就行，每一个群友最多一个称号，这一步类似 CSGO 的结算动画中给每一个小队成员的称号赋予。
可选的称号有如下的几个：

- 水群小能手: 进行发言，而且大部分都和技术没有关系的人
- 技术专家: 贡献技术相关的话题的人，且主导了对话内容
- 夜猫子: 经常在凌晨发言的人
- 表情包批发商: 经常发表情包的人，获取图片的功能暂时没有实现，这个称号你现在不应该赋予任何人
- KOL: 在某一个话题非常有发言权的关键人物
- ... (你可以自行进行拓展添加)

"""


@mcp.tool(
    description="对一段群聊消息进行总结，输出统计和成就称号"
)
def summarize_chat(params: SummarizeChatParams) -> Dict:
    return params.model_dump()


@mcp.tool(
    description='总结群友的聊天表现'
)
def summarize_user(params: SummarizeUserParams) -> Dict:
    return params.model_dump()


if __name__ == "__main__":
    mcp.run()
