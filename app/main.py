from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api.v1.api import api_router
from .core.redis import init_redis_pool

app = FastAPI(
    title="Matrix Flag",
    description="Feature Flag & Remote Config Service",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    await init_redis_pool()

@app.on_event("shutdown")
async def shutdown_event():
    pass

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 