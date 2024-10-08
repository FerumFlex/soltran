from services.base import BaseService


class SolanaCloud(BaseService):

    def __init__(self) -> None:
        super().__init__("https://token-list-api.solana.cloud")

    async def search_token_by_name(self, token_name) -> list[dict]:
        params = {
            "query": token_name,
            "chainId": 101,
            "start": 0,
            "limit": 20,
        }
        data = await self._request("get", "/v1/search", data=params)
        return data["content"]
