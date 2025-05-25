from crawl4ai import AsyncWebCrawler
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("crawl4ai-mcp")

@mcp.tool(
    name='get_web_markdown',
    description='获取网页的主体内容，并转换为Markdown格式。'
)
async def get_web_markdown(url: str) -> str:
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url
        )
        return result.markdown