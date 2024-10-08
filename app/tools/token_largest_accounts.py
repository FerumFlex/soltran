from langchain.agents import Tool
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from pydantic import BaseModel, Field

from tools import utils
from config import settings


class TokenAccount(BaseModel):
    address: str = Field(description="Owner address.")
    amount: float = Field(description="amount in tokens that account owns")


async def get_token_largest_accounts_func(token_addr: str) -> list[TokenAccount]:
    pub_key = Pubkey.from_string(token_addr)
    async with AsyncClient(settings.solana_endpoint_url) as client:
        res = await client.get_token_largest_accounts(pub_key)

    result = [
        TokenAccount(
            address=str(row.address),
            amount=utils.convert_to_tokens(row.amount.amount, row.amount.decimals),
        ) for row in res.value
    ]
    return result


token_largest_accounts_tool = Tool(
    name="get_token_largest_accounts",
    func=get_token_largest_accounts_func,
    coroutine=get_token_largest_accounts_func,
    description="Get largest accounts for particular token."
)
