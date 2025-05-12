from pydantic import BaseModel, Field, ConfigDict
from typing import List


class TokenInfo(BaseModel):
    address: str
    name: str
    symbol: str


class Liquidity(BaseModel):
    usd: float
    base: float
    quote: float


class Pool(BaseModel):
    chain_id: str = Field(..., alias="chainId")
    dex_id: str = Field(..., alias="dexId")
    url: str
    pair_address: str = Field(..., alias="pairAddress")
    labels: List[str]
    base_token: TokenInfo = Field(..., alias="baseToken")
    quote_token: TokenInfo = Field(..., alias="quoteToken")
    price_native: float = Field(..., alias="priceNative")
    price_usd: float = Field(..., alias="priceUsd")
    liquidity: Liquidity

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)


class TokenSummary(BaseModel):
    largest_pool: Pool
    total_liquidity_usd: float
    number_of_pools: int
