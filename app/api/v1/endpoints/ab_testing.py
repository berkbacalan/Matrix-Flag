from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from ...core.deps import get_current_manager_user
from ...models.ab_testing import (
    Experiment, ExperimentStatus, ExperimentResult
)
from ...services.ab_testing import ab_testing_service

router = APIRouter()

@router.post("/experiments", response_model=Experiment)
async def create_experiment(
    experiment: Experiment,
    current_user = Depends(get_current_manager_user)
):
    """Create a new A/B test experiment."""
    existing_experiment = await ab_testing_service.get_experiment(experiment.name)
    if existing_experiment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Experiment with this name already exists"
        )
    return await ab_testing_service.create_experiment(experiment)

@router.get("/experiments", response_model=List[Experiment])
async def list_experiments(
    current_user = Depends(get_current_manager_user)
):
    """List all A/B test experiments."""
    return await ab_testing_service.list_experiments()

@router.get("/experiments/{name}", response_model=Experiment)
async def get_experiment(
    name: str,
    current_user = Depends(get_current_manager_user)
):
    """Get a specific A/B test experiment."""
    experiment = await ab_testing_service.get_experiment(name)
    if not experiment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment not found"
        )
    return experiment

@router.put("/experiments/{name}", response_model=Experiment)
async def update_experiment(
    name: str,
    experiment: Experiment,
    current_user = Depends(get_current_manager_user)
):
    """Update an A/B test experiment."""
    updated_experiment = await ab_testing_service.update_experiment(name, experiment)
    if not updated_experiment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment not found"
        )
    return updated_experiment

@router.delete("/experiments/{name}")
async def delete_experiment(
    name: str,
    current_user = Depends(get_current_manager_user)
):
    """Delete an A/B test experiment."""
    success = await ab_testing_service.delete_experiment(name)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment not found"
        )
    return {"status": "success"}

@router.post("/experiments/{name}/assign")
async def assign_variant(
    name: str,
    user_id: str,
    context: Dict[str, Any],
    current_user = Depends(get_current_manager_user)
):
    """Assign a variant to a user for an experiment."""
    variant_name = await ab_testing_service.assign_variant(name, user_id, context)
    if not variant_name:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment not found or not running"
        )
    return {"variant_name": variant_name}

@router.post("/experiments/{name}/metrics")
async def record_metric(
    name: str,
    variant_name: str,
    metric_name: str,
    value: float,
    current_user = Depends(get_current_manager_user)
):
    """Record a metric value for an experiment variant."""
    experiment = await ab_testing_service.get_experiment(name)
    if not experiment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment not found"
        )
    if metric_name not in experiment.metrics:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid metric name for this experiment"
        )
    await ab_testing_service.record_metric(name, variant_name, metric_name, value)
    return {"status": "success"}

@router.get("/experiments/{name}/results", response_model=List[ExperimentResult])
async def get_experiment_results(
    name: str,
    current_user = Depends(get_current_manager_user)
):
    """Get the results of an A/B test experiment."""
    experiment = await ab_testing_service.get_experiment(name)
    if not experiment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment not found"
        )
    return await ab_testing_service.get_experiment_results(name) 