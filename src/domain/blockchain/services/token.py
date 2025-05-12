from typing import List

from domain.blockchain.models.token import TokenSummary, Pool
from domain.blockchain.services.pool import IDexScreenerPoolService


class DexscreenerService:
    def __init__(self, pool_service: IDexScreenerPoolService):
        self.pool_service = pool_service

    async def get_token_summary(
        self, chain_id: str, token_address: str
    ) -> TokenSummary:
        pools: List[Pool] = await self.pool_service.fetch_pools(
            chain_id, token_address
        )
        if not pools:
            raise ValueError(
                f"No pools found for {token_address} on {chain_id}"
            )

        total_usd = sum(pool.liquidity.usd for pool in pools)
        largest = max(pools, key=lambda pool: pool.liquidity.usd)
        return TokenSummary(
            largest_pool=largest,
            total_liquidity_usd=total_usd,
            number_of_pools=len(pools),
        )
