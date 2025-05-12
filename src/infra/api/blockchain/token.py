import httpx

from domain.blockchain.models.token import TokenSummary
from domain.blockchain.repositories.pool import DexscreenerPoolRepository
from domain.blockchain.services.token import DexscreenerService
from infra.app import app


@app.get("/chains/{chain_id}/tokens/{token_address}")
async def token_api(chain_id: str, token_address: str) -> TokenSummary:
    service = DexscreenerService(DexscreenerPoolRepository(httpx.AsyncClient()))
    return await service.get_token_summary(chain_id, token_address)
