from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json
import statistics
from ..core.redis import get_redis
from ..models.analytics import (
    MetricDefinition,
    MetricValue,
    MetricAggregation,
    Dashboard,
    Report,
    ReportResult,
    TimeRange,
)


class AnalyticsService:
    def __init__(self):
        self.redis = None

    async def _get_redis(self):
        if self.redis is None:
            self.redis = await get_redis()
        return self.redis

    async def create_metric(self, metric: MetricDefinition) -> MetricDefinition:
        """Create a new metric definition."""
        redis = await self._get_redis()
        metric_dict = metric.model_dump()
        await redis.hset(f"metric:{metric.name}", mapping=metric_dict)
        await redis.sadd("metrics", metric.name)
        return metric

    async def get_metric(self, name: str) -> Optional[MetricDefinition]:
        """Get a metric definition by name."""
        redis = await self._get_redis()
        metric_data = await redis.hgetall(f"metric:{name}")
        if not metric_data:
            return None
        return MetricDefinition(**metric_data)

    async def list_metrics(self) -> List[MetricDefinition]:
        """List all metric definitions."""
        redis = await self._get_redis()
        metric_names = await redis.smembers("metrics")
        metrics = []
        for name in metric_names:
            metric_data = await redis.hgetall(f"metric:{name}")
            if metric_data:
                metrics.append(MetricDefinition(**metric_data))
        return metrics

    async def record_metric(self, metric_value: MetricValue) -> None:
        """Record a metric value."""
        redis = await self._get_redis()
        metric_data = metric_value.model_dump()
        await redis.lpush(f"metric_values:{metric_value.metric_name}", json.dumps(metric_data))

    async def get_metric_values(
        self,
        metric_name: str,
        start_time: datetime,
        end_time: datetime,
        labels: Optional[Dict[str, str]] = None,
    ) -> List[MetricValue]:
        """Get metric values within a time range."""
        redis = await self._get_redis()
        values = await redis.lrange(f"metric_values:{metric_name}", 0, -1)
        metric_values = []

        for value in values:
            data = json.loads(value)
            timestamp = datetime.fromisoformat(data["timestamp"])
            if start_time <= timestamp <= end_time:
                if labels is None or all(data["labels"].get(k) == v for k, v in labels.items()):
                    metric_values.append(MetricValue(**data))

        return sorted(metric_values, key=lambda x: x.timestamp)

    async def aggregate_metric(
        self,
        metric_name: str,
        time_range: TimeRange,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        labels: Optional[Dict[str, str]] = None,
    ) -> MetricAggregation:
        """Aggregate metric values for a time range."""
        if end_time is None:
            end_time = datetime.utcnow()
        if start_time is None:
            if time_range == TimeRange.HOUR:
                start_time = end_time - timedelta(hours=1)
            elif time_range == TimeRange.DAY:
                start_time = end_time - timedelta(days=1)
            elif time_range == TimeRange.WEEK:
                start_time = end_time - timedelta(weeks=1)
            elif time_range == TimeRange.MONTH:
                start_time = end_time - timedelta(days=30)

        values = await self.get_metric_values(metric_name, start_time, end_time, labels)
        if not values:
            return MetricAggregation(
                metric_name=metric_name,
                time_range=time_range,
                start_time=start_time,
                end_time=end_time,
                values=[],
                labels=labels or {},
                count=0,
                sum=0,
                min=0,
                max=0,
                avg=0,
            )

        value_list = [v.value for v in values]
        return MetricAggregation(
            metric_name=metric_name,
            time_range=time_range,
            start_time=start_time,
            end_time=end_time,
            values=value_list,
            labels=labels or {},
            count=len(value_list),
            sum=sum(value_list),
            min=min(value_list),
            max=max(value_list),
            avg=statistics.mean(value_list),
        )

    async def create_dashboard(self, dashboard: Dashboard) -> Dashboard:
        """Create a new dashboard."""
        redis = await self._get_redis()
        dashboard_dict = dashboard.model_dump()
        await redis.hset(f"dashboard:{dashboard.name}", mapping=dashboard_dict)
        await redis.sadd("dashboards", dashboard.name)
        return dashboard

    async def get_dashboard(self, name: str) -> Optional[Dashboard]:
        """Get a dashboard by name."""
        redis = await self._get_redis()
        dashboard_data = await redis.hgetall(f"dashboard:{name}")
        if not dashboard_data:
            return None
        return Dashboard(**dashboard_data)

    async def update_dashboard(self, name: str, dashboard: Dashboard) -> Optional[Dashboard]:
        """Update an existing dashboard."""
        redis = await self._get_redis()
        existing_dashboard = await self.get_dashboard(name)
        if not existing_dashboard:
            return None

        dashboard_dict = dashboard.model_dump()
        dashboard_dict["updated_at"] = datetime.utcnow()
        await redis.hset(f"dashboard:{name}", mapping=dashboard_dict)
        return Dashboard(**dashboard_dict)

    async def delete_dashboard(self, name: str) -> bool:
        """Delete a dashboard."""
        redis = await self._get_redis()
        if not await redis.exists(f"dashboard:{name}"):
            return False
        await redis.delete(f"dashboard:{name}")
        await redis.srem("dashboards", name)
        return True

    async def list_dashboards(self) -> List[Dashboard]:
        """List all dashboards."""
        redis = await self._get_redis()
        dashboard_names = await redis.smembers("dashboards")
        dashboards = []
        for name in dashboard_names:
            dashboard_data = await redis.hgetall(f"dashboard:{name}")
            if dashboard_data:
                dashboards.append(Dashboard(**dashboard_data))
        return dashboards

    async def create_report(self, report: Report) -> Report:
        """Create a new report."""
        redis = await self._get_redis()
        report_dict = report.model_dump()
        await redis.hset(f"report:{report.name}", mapping=report_dict)
        await redis.sadd("reports", report.name)
        return report

    async def get_report(self, name: str) -> Optional[Report]:
        """Get a report by name."""
        redis = await self._get_redis()
        report_data = await redis.hgetall(f"report:{name}")
        if not report_data:
            return None
        return Report(**report_data)

    async def generate_report(self, name: str) -> ReportResult:
        """Generate a report."""
        report = await self.get_report(name)
        if not report:
            raise ValueError(f"Report {name} not found")

        start_time = report.start_time
        end_time = report.end_time or datetime.utcnow()

        metrics = {}
        for metric_name in report.metrics:
            try:
                aggregation = await self.aggregate_metric(
                    metric_name,
                    report.time_range,
                    start_time,
                    end_time,
                    report.filters,
                )
                metrics[metric_name] = aggregation
            except Exception as e:
                return ReportResult(
                    report_id=name,
                    metrics={},
                    execution_time=0,
                    status="error",
                    error=str(e),
                )

        return ReportResult(
            report_id=name,
            metrics=metrics,
            execution_time=0,  # TODO: Implement execution time tracking
            status="success",
        )


analytics_service = AnalyticsService()
