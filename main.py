from fastapi import FastAPI

from app.routers.auth import router as auth_router


app = FastAPI(title="MarketStall Backend Security Module")
# Routers are mounted centrally here so docs and tests share the same app instance.
app.include_router(auth_router)
