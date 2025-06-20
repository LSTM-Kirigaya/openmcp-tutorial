from crawl4ai import AsyncWebCrawler
from mcp.server.fastmcp import FastMCP
from crawl4ai.async_configs import BrowserConfig

mcp = FastMCP("crawl4ai-mcp")

# Using proxy URL
browser_config = BrowserConfig()

@mcp.tool(
    name='get_web_markdown',
    description='获取网页的主体内容，并转换为Markdown格式。'
)
async def get_web_markdown(url: str) -> str:
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url=url
        )

        return str(result.markdown)


@mcp.prompt(
    name='hacknews',
    description='获取HackNews的内容'
)
async def get_hacknews(topn: int = 3) -> str:
    return f'''
请帮我搜集 https://news.ycombinator.com/ 最热门的前 {topn} 条信息。

请一步步寻找，先罗列当前页面所有的超链接。

然后帮我进入这些网站后总结相关信息，返回翻译好的简体中文，并且整理成一个简单的资讯。
按以下格式输出（严格禁止添加任何额外引导语或总结句）：

[用一句吸引人的话开头，例如："⌨️ 今日份 AI & CS 技术文章分享"]

📌 [翻译成简体中文的文章标题]
摘要：[文章的核心观点，100字以内]
作者：[若存在]
发布时间：[若存在]
链接：[文章URL]
    '''