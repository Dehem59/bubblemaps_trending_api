import pytest

from domain.blockchain.models.token import Pool, TokenInfo, Liquidity
from domain.blockchain.services.pool import IDexScreenerPoolService
from domain.blockchain.services.token import DexscreenerService


class FakePoolService(IDexScreenerPoolService):
    def __init__(self, pools):
        self._pools = pools

    async def fetch_pools(self, chain_id: str, token_address: str):
        return self._pools


@pytest.mark.asyncio
async def test_single_pool_summary():
    pool = Pool(
        chain_id="solana",
        dex_id="raydium",
        url="https://example.com",
        pair_address="addr1",
        labels=["A"],
        base_token=TokenInfo(address="b", name="Base", symbol="B"),
        quote_token=TokenInfo(address="q", name="Quote", symbol="Q"),
        price_native=1.0,
        price_usd=10.0,
        liquidity=Liquidity(usd=500.0, base=50.0, quote=50.0),
    )
    service = DexscreenerService(FakePoolService([pool]))
    summary = await service.get_token_summary("solana", "token1")
    assert summary.number_of_pools == 1
    assert summary.total_liquidity_usd == 500.0
    assert summary.largest_pool == pool


@pytest.mark.asyncio
async def test_multiple_pools_summary():
    pool1 = Pool(
        chain_id="solana",
        dex_id="raydium",
        url="https://example.com",
        pair_address="addr1",
        labels=["A"],
        base_token=TokenInfo(address="b1", name="Base1", symbol="B1"),
        quote_token=TokenInfo(address="q1", name="Quote1", symbol="Q1"),
        price_native=1.0,
        price_usd=10.0,
        liquidity=Liquidity(usd=500.0, base=50.0, quote=50.0),
    )
    pool2 = Pool(
        chain_id="solana",
        dex_id="serum",
        url="https://example.org",
        pair_address="addr2",
        labels=["B"],
        base_token=TokenInfo(address="b2", name="Base2", symbol="B2"),
        quote_token=TokenInfo(address="q2", name="Quote2", symbol="Q2"),
        price_native=2.0,
        price_usd=20.0,
        liquidity=Liquidity(usd=1500.0, base=150.0, quote=150.0),
    )
    service = DexscreenerService(FakePoolService([pool1, pool2]))
    summary = await service.get_token_summary("solana", "token2")
    assert summary.number_of_pools == 2
    assert summary.total_liquidity_usd == 2000.0
    assert summary.largest_pool == pool2
