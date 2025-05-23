from fastapi import APIRouter
from .endpoints import feature_flags, auth

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(feature_flags.router, prefix="/flags", tags=["feature-flags"]) 