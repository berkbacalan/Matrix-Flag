from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router
from app.core.redis import init_redis_pool
from app.core.metrics import metrics_middleware, metrics_endpoint

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Feature Flag & Remote Config Service",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(metrics_middleware())

app.get("/metrics")(metrics_endpoint)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup_event():
    await init_redis_pool()


@app.on_event("shutdown")
async def shutdown_event():
    pass


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
