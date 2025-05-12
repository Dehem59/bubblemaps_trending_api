import pytest

from domain.blockchain.models.token import Pool, TokenInfo, Liquidity
from domain.blockchain.repositories.pool import IDexScreenerPoolRepository
from domain.blockchain.services.token import DexscreenerService


class FakePoolRepository(IDexScreenerPoolRepository):
    def __init__(self, pools):
        self._pools = pools

    async def fetch_token_pools(self, chain_id: str, token_address: str):
        return self._pools

    async def fetch_tokens_pools(self, chain_id: str, token_address: str):
        return self._pools


@pytest.mark.asyncio
async def test_single_pool_summary():
    pool = Pool(
        chain_id="solana",
        dex_id="raydium",
        url="https://example.com",
        pair_address="addr1",
        labels=["A"],
        base_token=TokenInfo(address="token", name="token", symbol="B"),
        quote_token=TokenInfo(address="q", name="Quote", symbol="Q"),
        price_native=1.0,
        price_usd=10.0,
        liquidity=Liquidity(usd=500.0, base=50.0, quote=50.0),
    )
    service = DexscreenerService(FakePoolRepository([pool]))
    summary = await service.get_token_summary("solana", "token")
    assert summary.number_of_pools == 1
    assert summary.total_liquidity_usd == 500.0
    assert summary.largest_pool == pool
    assert summary.token == pool.base_token


@pytest.mark.asyncio
async def test_multiple_pools_summary():
    pool1 = Pool(
        chain_id="solana",
        dex_id="raydium",
        url="https://example.com",
        pair_address="addr1",
        labels=["A"],
        base_token=TokenInfo(address="token1", name="token1", symbol="B1"),
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
        base_token=TokenInfo(address="token1", name="token1", symbol="B1"),
        quote_token=TokenInfo(address="q2", name="Quote2", symbol="Q2"),
        price_native=2.0,
        price_usd=20.0,
        liquidity=Liquidity(usd=1500.0, base=150.0, quote=150.0),
    )
    service = DexscreenerService(FakePoolRepository([pool1, pool2]))
    summary = await service.get_token_summary("solana", "token2")
    assert summary.number_of_pools == 2
    assert summary.total_liquidity_usd == 2000.0
    assert summary.largest_pool == pool2
    assert summary.token == pool1.base_token


@pytest.mark.asyncio
async def test_multiple_tokens_pool_aggregation():
    pool1 = Pool(
        chain_id="solana",
        dex_id="raydium",
        url="https://example.com",
        pair_address="addr1",
        labels=["A"],
        base_token=TokenInfo(address="token1", name="token1", symbol="B1"),
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
        base_token=TokenInfo(address="token2", name="token2", symbol="B2"),
        quote_token=TokenInfo(address="q2", name="Quote2", symbol="Q2"),
        price_native=2.0,
        price_usd=20.0,
        liquidity=Liquidity(usd=500.0, base=150.0, quote=150.0),
    )
    pool3 = Pool(
        chain_id="solana",
        dex_id="serum",
        url="https://example.org",
        pair_address="addr2",
        labels=["B"],
        base_token=TokenInfo(address="token2", name="token2", symbol="B2"),
        quote_token=TokenInfo(address="q2", name="Quote2", symbol="Q2"),
        price_native=2.0,
        price_usd=20.0,
        liquidity=Liquidity(usd=1500.0, base=150.0, quote=150.0),
    )
    service = DexscreenerService(FakePoolRepository([pool1, pool2, pool3]))
    summaries = await service.get_tokens_summaries("solana", ["token1", "token2"])

    summary_token_1 = next(
        filter(lambda summary: summary.token.address == "token1", summaries)
    )
    summary_token_2 = next(
        filter(lambda summary: summary.token.address == "token2", summaries)
    )

    assert summary_token_1.number_of_pools == 1
    assert summary_token_1.total_liquidity_usd == 500.0
    assert summary_token_1.largest_pool == pool1

    assert summary_token_2.number_of_pools == 2
    assert summary_token_2.total_liquidity_usd == 2000.0
    assert summary_token_2.largest_pool == pool3