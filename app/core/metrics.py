from prometheus_client import Counter, Histogram, Gauge, REGISTRY
from prometheus_client.openmetrics.exposition import generate_latest
from fastapi import Request, Response
import time
from typing import Callable

# HTTP Metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
)

# User Metrics
USER_OPERATIONS = Counter(
    "user_operations_total", "Total number of user operations", [
        "operation", "status"])

USER_LOGIN_ATTEMPTS = Counter(
    "user_login_attempts_total", "Total number of login attempts", ["status"]
)

ACTIVE_USERS = Gauge("active_users_total", "Total number of active users")

# Redis Metrics
REDIS_OPERATIONS = Counter(
    "redis_operations_total",
    "Total number of Redis operations",
    ["operation", "status"],
)

REDIS_OPERATION_LATENCY = Histogram(
    "redis_operation_duration_seconds",
    "Redis operation latency in seconds",
    ["operation"],
)

# System Metrics
SYSTEM_MEMORY_USAGE = Gauge(
    "system_memory_usage_bytes",
    "System memory usage in bytes")

SYSTEM_CPU_USAGE = Gauge(
    "system_cpu_usage_percent",
    "System CPU usage percentage")


def metrics_middleware():
    async def middleware(request: Request, call_next: Callable):
        start_time = time.time()

        try:
            response = await call_next(request)
            status = response.status_code
        except Exception as e:
            status = 500
            raise e
        finally:
            duration = time.time() - start_time
            REQUEST_COUNT.labels(
                method=request.method, endpoint=request.url.path, status=status
            ).inc()
            REQUEST_LATENCY.labels(
                method=request.method, endpoint=request.url.path
            ).observe(duration)

        return response

    return middleware


async def metrics_endpoint():
    return Response(generate_latest(REGISTRY), media_type="text/plain")


# Helper functions for metrics
def record_user_operation(operation: str, status: str):
    USER_OPERATIONS.labels(operation=operation, status=status).inc()


def record_login_attempt(status: str):
    USER_LOGIN_ATTEMPTS.labels(status=status).inc()


def update_active_users(count: int):
    ACTIVE_USERS.set(count)


def record_redis_operation(operation: str, status: str, duration: float):
    REDIS_OPERATIONS.labels(operation=operation, status=status).inc()
    REDIS_OPERATION_LATENCY.labels(operation=operation).observe(duration)


def update_system_metrics(memory_usage: float, cpu_usage: float):
    SYSTEM_MEMORY_USAGE.set(memory_usage)
    SYSTEM_CPU_USAGE.set(cpu_usage)
