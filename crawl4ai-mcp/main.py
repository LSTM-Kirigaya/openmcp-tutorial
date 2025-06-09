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