from langchain.agents import Tool
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from pydantic import BaseModel, Field

from tools import utils
from config import settings


class TokenSupply(BaseModel):
    amount: float = Field(description="Total supply in tokens.")
    decimals: int = Field(description="number of digits after the decimal point")


async def get_token_supply_func(token_addr: str) -> TokenSupply:
    pub_key = Pubkey.from_string(token_addr)
    async with AsyncClient(settings.solana_endpoint_url) as client:
        res = await client.get_token_supply(pub_key)
    return TokenSupply(
        amount=utils.convert_to_tokens(res.value.amount, res.value.decimals),
        decimals=res.value.decimals,
    )


token_supply_tool = Tool(
    name="get_token_supply",
    func=get_token_supply_func,
    coroutine=get_token_supply_func,
    description="Get token supply by addr."
)
