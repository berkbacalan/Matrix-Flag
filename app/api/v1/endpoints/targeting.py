from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.deps import get_current_manager_user
from app.models.targeting import (
    TargetingRule,
    TargetingRuleGroup,
    UserSegment,
    TargetingEvaluation,
)
from app.services.targeting import targeting_service

router = APIRouter()


@router.post("/rules", response_model=TargetingRule)
async def create_rule(
    rule: TargetingRule, current_user=Depends(get_current_manager_user)
):
    """Create a new targeting rule."""
    existing_rule = await targeting_service.get_rule(rule.name)
    if existing_rule:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rule with this name already exists",
        )
    return await targeting_service.create_rule(rule)


@router.get("/rules", response_model=List[TargetingRule])
async def list_rules(current_user=Depends(get_current_manager_user)):
    """List all targeting rules."""
    return await targeting_service.list_rules()


@router.get("/rules/{name}", response_model=TargetingRule)
async def get_rule(name: str, current_user=Depends(get_current_manager_user)):
    """Get a specific targeting rule."""
    rule = await targeting_service.get_rule(name)
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Rule not found"
        )
    return rule


@router.put("/rules/{name}", response_model=TargetingRule)
async def update_rule(
        name: str,
        rule: TargetingRule,
        current_user=Depends(get_current_manager_user)):
    """Update a targeting rule."""
    updated_rule = await targeting_service.update_rule(name, rule)
    if not updated_rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Rule not found"
        )
    return updated_rule


@router.delete("/rules/{name}")
async def delete_rule(
        name: str,
        current_user=Depends(get_current_manager_user)):
    """Delete a targeting rule."""
    success = await targeting_service.delete_rule(name)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Rule not found"
        )
    return {"status": "success"}


@router.post("/rules/evaluate", response_model=List[TargetingEvaluation])
async def evaluate_rules(
    rules: List[TargetingRule],
    context: Dict[str, Any],
    current_user=Depends(get_current_manager_user),
):
    """Evaluate a list of rules against a context."""
    return await targeting_service.evaluate_rules(rules, context)


@router.post("/segments", response_model=UserSegment)
async def create_segment(
    segment: UserSegment, current_user=Depends(get_current_manager_user)
):
    """Create a new user segment."""
    existing_segment = await targeting_service.get_segment(segment.name)
    if existing_segment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Segment with this name already exists",
        )
    return await targeting_service.create_segment(segment)


@router.get("/segments", response_model=List[UserSegment])
async def list_segments(current_user=Depends(get_current_manager_user)):
    """List all user segments."""
    return await targeting_service.list_segments()


@router.get("/segments/{name}", response_model=UserSegment)
async def get_segment(
        name: str,
        current_user=Depends(get_current_manager_user)):
    """Get a specific user segment."""
    segment = await targeting_service.get_segment(name)
    if not segment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Segment not found"
        )
    return segment


@router.put("/segments/{name}", response_model=UserSegment)
async def update_segment(
        name: str,
        segment: UserSegment,
        current_user=Depends(get_current_manager_user)):
    """Update a user segment."""
    updated_segment = await targeting_service.update_segment(name, segment)
    if not updated_segment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Segment not found"
        )
    return updated_segment


@router.delete("/segments/{name}")
async def delete_segment(
        name: str,
        current_user=Depends(get_current_manager_user)):
    """Delete a user segment."""
    success = await targeting_service.delete_segment(name)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Segment not found"
        )
    return {"status": "success"}
