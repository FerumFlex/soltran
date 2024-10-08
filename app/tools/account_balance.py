from langchain.agents import Tool

from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey

from config import settings
from tools import utils


async def get_account_balance_func(addr: str) -> int:
    pub_key = Pubkey.from_string(addr)
    async with AsyncClient(settings.solana_endpoint_url) as client:
        res = await client.get_balance(pub_key)
    return utils.convert_to_solana(res.value)


account_balance_tool = Tool(
    name="get_account_balance",
    func=get_account_balance_func,
    coroutine=get_account_balance_func,
    description="Get solana account balance by addr. Result in SOL. Example of address is H6Vb6qdn4pfg1tmqXhVK8WQocsfeUWRhTNZFMjeypsRE."
)
