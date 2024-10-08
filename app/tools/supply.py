from langchain.agents import Tool
from solana.rpc.async_api import AsyncClient
from pydantic import BaseModel, Field

from tools import utils
from config import settings


class Supply(BaseModel):
    total: float = Field(description="Total supply in SOL.")
    circulating: float = Field(description="Total circulating in SOL.")
    non_circulating: float = Field(description="Total non circulating in SOL.")


async def get_supply_func(*args) -> Supply:
    async with AsyncClient(settings.solana_endpoint_url) as client:
        res = await client.get_supply()
    return Supply(
        total=utils.convert_to_solana(res.value.total),
        circulating=utils.convert_to_solana(res.value.circulating),
        non_circulating=utils.convert_to_solana(res.value.non_circulating),
    )


supply_tool = Tool(
    name="get_supply",
    func=get_supply_func,
    coroutine=get_supply_func,
    description="Get current solana supply in SOL."
)
