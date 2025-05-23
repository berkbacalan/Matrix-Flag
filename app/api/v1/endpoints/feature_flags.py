from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.deps import get_current_manager_user
from app.models.feature_flag import (
    FeatureFlag, FeatureFlagUpdate, WebhookEvent,
    FlagType
)
from app.services.feature_flag import feature_flag_service

router = APIRouter()

@router.post("/", response_model=FeatureFlag)
async def create_flag(flag: FeatureFlag):
    existing_flag = await feature_flag_service.get_flag(flag.key)
    if existing_flag:
        raise HTTPException(status_code=400, detail="Flag with this key already exists")
    return await feature_flag_service.create_flag(flag)

@router.get("/{key}", response_model=FeatureFlag)
async def get_flag(key: str):
    flag = await feature_flag_service.get_flag(key)
    if not flag:
        raise HTTPException(status_code=404, detail="Flag not found")
    return flag

@router.put("/{key}", response_model=FeatureFlag)
async def update_flag(key: str, update: FeatureFlagUpdate):
    flag = await feature_flag_service.update_flag(key, update)
    if not flag:
        raise HTTPException(status_code=404, detail="Flag not found")
    return flag

@router.delete("/{key}")
async def delete_flag(key: str):
    success = await feature_flag_service.delete_flag(key)
    if not success:
        raise HTTPException(status_code=404, detail="Flag not found")
    return {"status": "success"}

@router.get("/", response_model=List[FeatureFlag])
async def list_flags():
    return await feature_flag_service.list_flags()

@router.post("/webhooks/{url}")
async def add_webhook(url: str):
    await feature_flag_service.add_webhook(url)
    return {"status": "success"}

@router.delete("/webhooks/{url}")
async def remove_webhook(url: str):
    await feature_flag_service.remove_webhook(url)
    return {"status": "success"} 