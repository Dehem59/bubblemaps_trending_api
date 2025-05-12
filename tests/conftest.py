from fastapi.testclient import TestClient

from infra.api.factories.http_client import get_http_client
from infra.app import app
import pytest

from tests.infra.fake import FakeHttpClient


@pytest.fixture(autouse=True)
def override_http_client():
    """
    Override the get_http_client dependency to yield our FakeHttpClient.
    """
    # Prepare fake payloads for two scenarios:
    single_token_url = "https://api.dexscreener.com/token-pairs/v1/solana/token1"
    multi_token_url = "https://api.dexscreener.com/tokens/v1/solana/addr1,addr2"

    # Minimal pool objects matching Pydantic model structure:
    pool_a = {
        "chainId": "solana",
        "dexId": "raydium",
        "url": "https://example.com/pairA",
        "pairAddress": "pairA",
        "labels": ["labelA"],
        "baseToken": {"address": "addr1", "name": "Token1", "symbol": "T1"},
        "quoteToken": {"address": "quote", "name": "USDC", "symbol": "USDC"},
        "priceNative": 1.0,
        "priceUsd": 5.0,
        "liquidity": {"usd": 100.0, "base": 10.0, "quote": 90.0},
    }
    pool_b = {
        "chainId": "solana",
        "dexId": "serum",
        "url": "https://example.com/pairB",
        "pairAddress": "pairB",
        "labels": ["labelB"],
        "baseToken": {"address": "addr2", "name": "Token2", "symbol": "T2"},
        "quoteToken": {"address": "quote", "name": "USDC", "symbol": "USDC"},
        "priceNative": 2.0,
        "priceUsd": 10.0,
        "liquidity": {"usd": 200.0, "base": 20.0, "quote": 180.0},
    }

    url_map = {
        single_token_url: [pool_a],
        multi_token_url: [pool_a, pool_b],
    }

    # Override the dependency
    app.dependency_overrides[get_http_client] = lambda: FakeHttpClient(url_map)
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def client():
    return TestClient(app)

