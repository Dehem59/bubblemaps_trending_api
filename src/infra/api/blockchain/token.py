from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from httpx import AsyncClient

from domain.blockchain.models.token import TokenSummary
from domain.blockchain.repositories.pool import DexscreenerPoolRepository
from domain.blockchain.services.token import DexscreenerService
from infra.api.factories.http_client import get_http_client

router = APIRouter(
    prefix="/chains/{chain_id}/tokens",
    tags=["tokens"],
)


@router.get("/{token_address}", response_model=TokenSummary)
async def get_token_summary(
    chain_id: str,
    token_address: str,
    client: AsyncClient = Depends(get_http_client),
):
    repo = DexscreenerPoolRepository(client)
    service = DexscreenerService(repo)
    try:
        return await service.get_token_summary(chain_id, token_address)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=List[TokenSummary])
async def get_tokens_summaries(
    chain_id: str,
    addresses: List[str] = Query(
        ...,
        description="Comma-separated list of token addresses",
        example="addr1,addr2,addr3",
    ),
    client: AsyncClient = Depends(get_http_client),
):
    """
    Returns for each token in `addresses` on `chain_id`:
     - largest_pool and its info
     - total_liquidity_usd
     - number_of_pools
    """
    if not addresses:
        raise HTTPException(status_code=400, detail="No addresses provided")
    repo = DexscreenerPoolRepository(client)
    service = DexscreenerService(repo)
    try:
        return await service.get_tokens_summaries(chain_id, addresses)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
