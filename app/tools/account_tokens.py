from langchain.agents import Tool
from config import settings

from solana.rpc.types import TokenAccountOpts
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey

from tools import utils


async def get_account_tokens_func(addr: str) -> str:
    pub_key = Pubkey.from_string(addr)
    token_account_opts = TokenAccountOpts(program_id=Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"))
    async with AsyncClient(settings.solana_endpoint_url) as client:
        res = await client.get_token_accounts_by_owner_json_parsed(pub_key, token_account_opts)

        # # gather token addresses
        # token_addresses = []
        # for row in res.value:
        #     amount = row.account.data.parsed["info"]["tokenAmount"]["uiAmount"]
        #     if amount <= 0:
        #         continue

        #     token_addr = Pubkey.from_string(row.account.data.parsed["info"]["mint"])
        #     token_addresses.append(token_addr)

        # # raise Exception(token_addresses)

        # token_names = {}
        # res2 = await client.get_multiple_accounts_json_parsed(token_addresses)
        # for row in res2:
        #     mint = row.value.data.parsed["info"]["mint"]
        #     token_names[mint] = row.value.parsed["info"]["name"]
        # raise Exception(token_names)

    parts = []
    for row in res.value:
        amount = row.account.data.parsed["info"]["tokenAmount"]["uiAmount"]
        if amount <= 0:
            continue

        token_addr = row.account.data.parsed["info"]["mint"]
        decimals = row.account.data.parsed["info"]["tokenAmount"]["decimals"]
        token_amount = utils.convert_to_tokens(amount, decimals)
        row_str = f"{token_addr} {token_amount}"
        parts.append(row_str)

    return "\n".join(parts)


account_tokens_tool = Tool(
    name="get_account_tokens",
    func=get_account_tokens_func,
    coroutine=get_account_tokens_func,
    description="Get list of tokens by addr. Example of address is H6Vb6qdn4pfg1tmqXhVK8WQocsfeUWRhTNZFMjeypsRE."
)
