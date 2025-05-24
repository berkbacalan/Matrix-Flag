from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timedelta
from app.models.analytics import (
    MetricDefinition,
    MetricValue,
    MetricAggregation,
    Dashboard,
    Widget,
    Report,
    ReportResult,
    TimeRange,
)
from app.services.analytics import analytics_service
from app.core.deps import get_current_manager_user

router = APIRouter()


# Metric endpoints
@router.post("/metrics", response_model=MetricDefinition)
async def create_metric(
    metric: MetricDefinition, current_user=Depends(get_current_manager_user)
):
    """Create a new metric definition."""
    return await analytics_service.create_metric(metric)


@router.get("/metrics", response_model=List[MetricDefinition])
async def list_metrics(current_user=Depends(get_current_manager_user)):
    """List all metric definitions."""
    return await analytics_service.list_metrics()


@router.get("/metrics/{name}", response_model=MetricDefinition)
async def get_metric(
        name: str,
        current_user=Depends(get_current_manager_user)):
    """Get a metric definition by name."""
    metric = await analytics_service.get_metric(name)
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    return metric


@router.post("/metrics/{name}/values")
async def record_metric_value(
    name: str,
    value: float,
    labels: Optional[Dict[str, str]] = None,
    current_user=Depends(get_current_manager_user),
):
    """Record a metric value."""
    metric_value = MetricValue(
        metric_name=name,
        value=value,
        labels=labels or {},
        timestamp=datetime.utcnow())
    await analytics_service.record_metric(metric_value)
    return {"status": "success"}


@router.get("/metrics/{name}/values", response_model=List[MetricValue])
async def get_metric_values(
    name: str,
    start_time: datetime = Query(...),
    end_time: datetime = Query(...),
    labels: Optional[Dict[str, str]] = None,
    current_user=Depends(get_current_manager_user),
):
    """Get metric values within a time range."""
    return await analytics_service.get_metric_values(name, start_time, end_time, labels)


@router.get("/metrics/{name}/aggregate", response_model=MetricAggregation)
async def aggregate_metric(
    name: str,
    time_range: TimeRange = Query(...),
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    labels: Optional[Dict[str, str]] = None,
    current_user=Depends(get_current_manager_user),
):
    """Aggregate metric values for a time range."""
    return await analytics_service.aggregate_metric(
        name, time_range, start_time, end_time, labels
    )


# Dashboard endpoints
@router.post("/dashboards", response_model=Dashboard)
async def create_dashboard(
    dashboard: Dashboard, current_user=Depends(get_current_manager_user)
):
    """Create a new dashboard."""
    return await analytics_service.create_dashboard(dashboard)


@router.get("/dashboards", response_model=List[Dashboard])
async def list_dashboards(current_user=Depends(get_current_manager_user)):
    """List all dashboards."""
    return await analytics_service.list_dashboards()


@router.get("/dashboards/{name}", response_model=Dashboard)
async def get_dashboard(
        name: str,
        current_user=Depends(get_current_manager_user)):
    """Get a dashboard by name."""
    dashboard = await analytics_service.get_dashboard(name)
    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return dashboard


@router.put("/dashboards/{name}", response_model=Dashboard)
async def update_dashboard(
        name: str,
        dashboard: Dashboard,
        current_user=Depends(get_current_manager_user)):
    """Update an existing dashboard."""
    updated_dashboard = await analytics_service.update_dashboard(name, dashboard)
    if not updated_dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return updated_dashboard


@router.delete("/dashboards/{name}")
async def delete_dashboard(
        name: str,
        current_user=Depends(get_current_manager_user)):
    """Delete a dashboard."""
    success = await analytics_service.delete_dashboard(name)
    if not success:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return {"status": "success"}


# Report endpoints
@router.post("/reports", response_model=Report)
async def create_report(
        report: Report,
        current_user=Depends(get_current_manager_user)):
    """Create a new report."""
    return await analytics_service.create_report(report)


@router.get("/reports/{name}", response_model=Report)
async def get_report(
        name: str,
        current_user=Depends(get_current_manager_user)):
    """Get a report by name."""
    report = await analytics_service.get_report(name)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.post("/reports/{name}/generate", response_model=ReportResult)
async def generate_report(
        name: str,
        current_user=Depends(get_current_manager_user)):
    """Generate a report."""
    try:
        return await analytics_service.generate_report(name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
