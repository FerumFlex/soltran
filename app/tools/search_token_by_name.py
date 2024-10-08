from langchain.agents import Tool

from services.solana_cloud import SolanaCloud


async def get_search_token_by_name_func(token_name: str) -> str:
    async with SolanaCloud() as client:
        res = await client.search_token_by_name(token_name)

    if res:
        return res[0]["address"]
    else:
        return "No token found."


search_token_by_name_tool = Tool(
    name="get_search_token_by_name",
    func=get_search_token_by_name_func,
    coroutine=get_search_token_by_name_func,
    description="Search token address by token name."
)
