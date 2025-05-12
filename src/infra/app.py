from fastapi import FastAPI
from infra.api.blockchain.token import router as token_router
app = FastAPI(title="BubbleMaps Trending API", root_path="/api")

app.include_router(token_router)
