from langchain.agents import Tool
from config import settings

from solana.rpc.async_api import AsyncClient


async def get_current_block_height_func(*args) -> int:
    async with AsyncClient(settings.solana_endpoint_url) as client:
        res = await client.get_block_height()
    return res.value


block_height_tool = Tool(
    name="get_current_block_height",
    func=get_current_block_height_func,
    coroutine=get_current_block_height_func,
    description="Get current block for solana blockchain."
)
