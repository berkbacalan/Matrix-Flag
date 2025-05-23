from fastapi import APIRouter
from .endpoints import auth, feature_flags, targeting, ab_testing

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(feature_flags.router, prefix="/flags", tags=["feature-flags"])
api_router.include_router(targeting.router, prefix="/targeting", tags=["targeting"])
api_router.include_router(ab_testing.router, prefix="/ab-testing", tags=["a-b-testing"]) 