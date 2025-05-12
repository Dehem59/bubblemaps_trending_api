from collections import defaultdict
from itertools import groupby
from typing import List, Dict

from domain.blockchain.models.token import TokenSummary, Pool
from domain.blockchain.repositories.pool import IDexScreenerPoolRepository


class DexscreenerService:
    def __init__(self, pool_service: IDexScreenerPoolRepository):
        self.pool_service = pool_service

    @staticmethod
    def aggregate_pool_data(pools: List[Pool]) -> TokenSummary:
        total_usd = sum(pool.liquidity.usd for pool in pools)
        largest = max(pools, key=lambda pool: pool.liquidity.usd)
        return TokenSummary(
            largest_pool=largest,
            total_liquidity_usd=total_usd,
            number_of_pools=len(pools),
            token=pools[0].base_token,
        )

    async def get_token_summary(
        self, chain_id: str, token_address: str
    ) -> TokenSummary:
        pools: List[Pool] = await self.pool_service.fetch_token_pools(
            chain_id, token_address
        )
        if not pools:
            raise ValueError(
                f"No pools found for {token_address} on {chain_id}"
            )
        return self.aggregate_pool_data(pools)

    async def get_tokens_summaries(
        self, chain_id: str, token_addresses: List[str]
    ) -> List[TokenSummary]:
        pools: List[Pool] = await self.pool_service.fetch_tokens_pools(
            chain_id, token_addresses
        )
        if not pools:
            raise ValueError(
                f"No pools found for {token_addresses} on {chain_id}"
            )
        grouped_pools = group_pools_by_token(pools)
        return [
            self.aggregate_pool_data(pools) for _, pools in grouped_pools.items()
        ]


def group_pools_by_token(pools: List[Pool]) -> Dict[str, List[Pool]]:
    result = defaultdict(list)
    for pool in pools:
        result[pool.base_token.address].append(pool)
    return result

