from langchain.agents import Tool
from config import settings

from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey


async def get_account_info_func(addr: str) -> str:
    pub_key = Pubkey.from_string(addr)
    async with AsyncClient(settings.solana_endpoint_url) as client:
        res = await client.get_account_info(pub_key)
    return res.to_json()


account_info_tool = Tool(
    name="get_account_info",
    func=get_account_info_func,
    coroutine=get_account_info_func,
    description="Get account info by addr. Example of address is H6Vb6qdn4pfg1tmqXhVK8WQocsfeUWRhTNZFMjeypsRE."
)
