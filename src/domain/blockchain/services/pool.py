from abc import ABC, abstractmethod
from typing import List
import httpx

from domain.blockchain.models.token import Pool


class IDexScreenerPoolService(ABC):
    @abstractmethod
    async def fetch_pools(self, chain_id: str, token_address: str) -> List[Pool]:
        ...


class DexscreenerPoolService(IDexScreenerPoolService):
    def __init__(
        self,
        http_client: httpx.AsyncClient,
        base_url: str = "https://api.dexscreener.com",
    ):
        self.client = http_client
        self.base_url = base_url

    async def fetch_pools(
        self, chain_id: str, token_address: str
    ) -> List[Pool]:
        url = f"{self.base_url}/token-pairs/v1/{chain_id}/{token_address}"
        response = await self.client.get(url)
        response.raise_for_status()
        data = response.json()
        return [Pool(**item) for item in data]
