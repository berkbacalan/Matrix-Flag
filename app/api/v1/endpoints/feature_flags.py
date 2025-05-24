from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.core.deps import get_current_manager_user
from app.models.feature_flag import (
    FeatureFlag, FeatureFlagUpdate, WebhookEvent,
    FlagType
)
from app.services.feature_flag import feature_flag_service

router = APIRouter()

@router.get("/", response_model=List[schemas.FeatureFlag])
async def list_feature_flags(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, description="Number of records to skip", ge=0),
    limit: int = Query(100, description="Maximum number of records to return", ge=1, le=100),
    project_id: Optional[int] = Query(None, description="Filter by project ID"),
    environment: Optional[str] = Query(None, description="Filter by environment (e.g., 'production', 'staging')"),
    is_active: Optional[bool] = Query(None, description="Filter by active status")
) -> List[schemas.FeatureFlag]:
    """
    Retrieve a list of feature flags with optional filtering.
    
    Parameters:
    - skip: Number of records to skip (pagination)
    - limit: Maximum number of records to return (pagination)
    - project_id: Filter by specific project
    - environment: Filter by environment
    - is_active: Filter by active status
    
    Returns:
    - List of feature flags matching the criteria
    
    Example:
    ```python
    # Get all active feature flags in production
    flags = await client.list_feature_flags(
        environment="production",
        is_active=True
    )
    ```
    """
    return await crud.feature_flag.get_multi(
        db, skip=skip, limit=limit,
        project_id=project_id,
        environment=environment,
        is_active=is_active
    )

@router.post("/", response_model=schemas.FeatureFlag)
async def create_feature_flag(
    *,
    db: Session = Depends(deps.get_db),
    feature_flag_in: schemas.FeatureFlagCreate,
    current_user: models.User = Depends(deps.get_current_active_user)
) -> schemas.FeatureFlag:
    """
    Create a new feature flag.
    
    Parameters:
    - feature_flag_in: Feature flag data
    
    Returns:
    - Created feature flag
    
    Example:
    ```python
    # Create a new feature flag
    new_flag = await client.create_feature_flag(
        name="new-feature",
        description="Enable new feature",
        is_active=True,
        environment="production"
    )
    ```
    """
    return await crud.feature_flag.create(db, obj_in=feature_flag_in)

@router.get("/{feature_flag_id}", response_model=schemas.FeatureFlag)
async def get_feature_flag(
    feature_flag_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> schemas.FeatureFlag:
    """
    Get a specific feature flag by ID.
    
    Parameters:
    - feature_flag_id: ID of the feature flag
    
    Returns:
    - Feature flag details
    
    Raises:
    - HTTPException: If feature flag not found
    
    Example:
    ```python
    # Get feature flag by ID
    flag = await client.get_feature_flag(feature_flag_id=1)
    ```
    """
    feature_flag = await crud.feature_flag.get(db, id=feature_flag_id)
    if not feature_flag:
        raise HTTPException(status_code=404, detail="Feature flag not found")
    return feature_flag

@router.put("/{feature_flag_id}", response_model=schemas.FeatureFlag)
async def update_feature_flag(
    *,
    db: Session = Depends(deps.get_db),
    feature_flag_id: int,
    feature_flag_in: schemas.FeatureFlagUpdate,
    current_user: models.User = Depends(deps.get_current_active_user)
) -> schemas.FeatureFlag:
    """
    Update a feature flag.
    
    Parameters:
    - feature_flag_id: ID of the feature flag to update
    - feature_flag_in: Updated feature flag data
    
    Returns:
    - Updated feature flag
    
    Raises:
    - HTTPException: If feature flag not found
    
    Example:
    ```python
    # Update feature flag
    updated_flag = await client.update_feature_flag(
        feature_flag_id=1,
        is_active=False,
        description="Updated description"
    )
    ```
    """
    feature_flag = await crud.feature_flag.get(db, id=feature_flag_id)
    if not feature_flag:
        raise HTTPException(status_code=404, detail="Feature flag not found")
    return await crud.feature_flag.update(db, db_obj=feature_flag, obj_in=feature_flag_in)

@router.delete("/{feature_flag_id}", response_model=schemas.FeatureFlag)
async def delete_feature_flag(
    *,
    db: Session = Depends(deps.get_db),
    feature_flag_id: int,
    current_user: models.User = Depends(deps.get_current_active_user)
) -> schemas.FeatureFlag:
    """
    Delete a feature flag.
    
    Parameters:
    - feature_flag_id: ID of the feature flag to delete
    
    Returns:
    - Deleted feature flag
    
    Raises:
    - HTTPException: If feature flag not found
    
    Example:
    ```python
    # Delete feature flag
    deleted_flag = await client.delete_feature_flag(feature_flag_id=1)
    ```
    """
    feature_flag = await crud.feature_flag.get(db, id=feature_flag_id)
    if not feature_flag:
        raise HTTPException(status_code=404, detail="Feature flag not found")
    return await crud.feature_flag.remove(db, id=feature_flag_id)

@router.post("/{feature_flag_id}/toggle", response_model=schemas.FeatureFlag)
async def toggle_feature_flag(
    *,
    db: Session = Depends(deps.get_db),
    feature_flag_id: int,
    current_user: models.User = Depends(deps.get_current_active_user)
) -> schemas.FeatureFlag:
    """
    Toggle a feature flag's active status.
    
    Parameters:
    - feature_flag_id: ID of the feature flag to toggle
    
    Returns:
    - Updated feature flag
    
    Raises:
    - HTTPException: If feature flag not found
    
    Example:
    ```python
    # Toggle feature flag
    toggled_flag = await client.toggle_feature_flag(feature_flag_id=1)
    ```
    """
    feature_flag = await crud.feature_flag.get(db, id=feature_flag_id)
    if not feature_flag:
        raise HTTPException(status_code=404, detail="Feature flag not found")
    return await crud.feature_flag.toggle(db, db_obj=feature_flag)

@router.post("/webhooks/{url}")
async def add_webhook(url: str):
    await feature_flag_service.add_webhook(url)
    return {"status": "success"}

@router.delete("/webhooks/{url}")
async def remove_webhook(url: str):
    await feature_flag_service.remove_webhook(url)
    return {"status": "success"} 