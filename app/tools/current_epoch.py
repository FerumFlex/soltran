from langchain.agents import Tool
from config import settings

from solana.rpc.async_api import AsyncClient


async def get_current_epoch_func(*args) -> str:
    async with AsyncClient(settings.solana_endpoint_url) as client:
        res = await client.get_epoch_info()
    return res.to_json()


current_epoch_info_tool = Tool(
    name="get_current_epoch_info",
    func=get_current_epoch_func,
    coroutine=get_current_epoch_func,
    description="Get current epoch info for solana blockchain."
)
