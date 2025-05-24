from typing import List, Dict, Any, Optional
from datetime import datetime
import hashlib
import json
import random
import statistics
from ..core.redis import get_redis
from ..models.ab_testing import (
    Experiment,
    ExperimentStatus,
    ExperimentAssignment,
    MetricValue,
    ExperimentResult,
)
from .targeting import targeting_service


class ABTestingService:
    def __init__(self):
        self.redis = None

    async def _get_redis(self):
        if self.redis is None:
            self.redis = await get_redis()
        return self.redis

    def _calculate_variant_assignment(
        self, experiment: Experiment, user_id: str
    ) -> str:
        """Calculate which variant a user should be assigned to based on weights."""
        if not experiment.variants:
            raise ValueError("Experiment must have at least one variant")

        # Create a deterministic hash based on experiment name and user ID
        hash_input = f"{experiment.name}:{user_id}"
        hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
        random.seed(hash_value)

        # Calculate total weight and create weighted distribution
        total_weight = sum(variant.weight for variant in experiment.variants)
        weights = [
            variant.weight /
            total_weight for variant in experiment.variants]

        # Select variant based on weights
        selected_variant = random.choices(
            [variant.name for variant in experiment.variants], weights=weights, k=1
        )[0]

        return selected_variant

    async def create_experiment(self, experiment: Experiment) -> Experiment:
        """Create a new A/B test experiment."""
        redis = await self._get_redis()

        # Validate experiment
        if not experiment.variants:
            raise ValueError("Experiment must have at least one variant")

        # Store experiment
        experiment_dict = experiment.model_dump()
        await redis.hset(f"experiment:{experiment.name}", mapping=experiment_dict)
        await redis.sadd("experiments", experiment.name)

        return experiment

    async def get_experiment(self, name: str) -> Optional[Experiment]:
        """Get an experiment by name."""
        redis = await self._get_redis()
        experiment_data = await redis.hgetall(f"experiment:{name}")
        if not experiment_data:
            return None
        return Experiment(**experiment_data)

    async def update_experiment(
        self, name: str, experiment: Experiment
    ) -> Optional[Experiment]:
        """Update an existing experiment."""
        redis = await self._get_redis()
        existing_experiment = await self.get_experiment(name)
        if not existing_experiment:
            return None

        experiment_dict = experiment.model_dump()
        experiment_dict["updated_at"] = datetime.utcnow()
        await redis.hset(f"experiment:{name}", mapping=experiment_dict)
        return Experiment(**experiment_dict)

    async def delete_experiment(self, name: str) -> bool:
        """Delete an experiment."""
        redis = await self._get_redis()
        if not await redis.exists(f"experiment:{name}"):
            return False
        await redis.delete(f"experiment:{name}")
        await redis.srem("experiments", name)
        return True

    async def list_experiments(self) -> List[Experiment]:
        """List all experiments."""
        redis = await self._get_redis()
        experiment_names = await redis.smembers("experiments")
        experiments = []
        for name in experiment_names:
            experiment_data = await redis.hgetall(f"experiment:{name}")
            if experiment_data:
                experiments.append(Experiment(**experiment_data))
        return experiments

    async def assign_variant(
        self, experiment_name: str, user_id: str, context: Dict[str, Any]
    ) -> Optional[str]:
        """Assign a variant to a user for an experiment."""
        experiment = await self.get_experiment(experiment_name)
        if not experiment or experiment.status != ExperimentStatus.RUNNING:
            return None

        # Check if user is already assigned
        redis = await self._get_redis()
        assignment_key = f"experiment_assignment:{experiment_name}:{user_id}"
        existing_assignment = await redis.get(assignment_key)
        if existing_assignment:
            return existing_assignment.decode()

        # Check targeting rules
        if experiment.targeting_rules:
            rules = []
            for rule_name in experiment.targeting_rules:
                rule = await targeting_service.get_rule(rule_name)
                if rule:
                    rules.append(rule)

            evaluations = await targeting_service.evaluate_rules(rules, context)
            if not any(eval.result for eval in evaluations):
                return None

        # Assign variant
        variant_name = self._calculate_variant_assignment(experiment, user_id)

        # Store assignment
        assignment = ExperimentAssignment(
            experiment_id=experiment_name,
            user_id=user_id,
            variant_name=variant_name)
        await redis.set(assignment_key, variant_name)
        await redis.hset(
            f"experiment_assignments:{experiment_name}",
            user_id,
            assignment.model_dump_json(),
        )

        return variant_name

    async def record_metric(
            self,
            experiment_name: str,
            variant_name: str,
            metric_name: str,
            value: float) -> None:
        """Record a metric value for an experiment variant."""
        redis = await self._get_redis()
        metric = MetricValue(
            experiment_id=experiment_name,
            variant_name=variant_name,
            metric_name=metric_name,
            value=value,
        )
        await redis.lpush(
            f"experiment_metrics:{experiment_name}:{variant_name}:{metric_name}",
            metric.model_dump_json(),
        )

    async def get_experiment_results(
        self, experiment_name: str
    ) -> List[ExperimentResult]:
        """Calculate and return experiment results."""
        redis = await self._get_redis()
        experiment = await self.get_experiment(experiment_name)
        if not experiment:
            return []

        results = []
        for variant in experiment.variants:
            # Get all assignments for this variant
            assignments = await redis.hgetall(
                f"experiment_assignments:{experiment_name}"
            )
            variant_users = [
                user_id
                for user_id, assignment in assignments.items()
                if json.loads(assignment)["variant_name"] == variant.name
            ]
            total_users = len(variant_users)

            # Calculate metrics
            metrics = {}
            for metric_name in experiment.metrics:
                metric_values = []
                for user_id in variant_users:
                    values = await redis.lrange(
                        f"experiment_metrics:{experiment_name}:{variant.name}:{metric_name}",
                        0,
                        -1,
                    )
                    if values:
                        metric_values.extend(
                            [json.loads(v)["value"] for v in values])

                if metric_values:
                    mean = statistics.mean(metric_values)
                    stdev = (statistics.stdev(metric_values)
                             if len(metric_values) > 1 else 0)
                    confidence_interval = 1.96 * \
                        (stdev / (len(metric_values) ** 0.5))

                    metrics[metric_name] = {
                        "value": mean,
                        "confidence_interval": confidence_interval,
                    }

            result = ExperimentResult(
                experiment_id=experiment_name,
                variant_name=variant.name,
                total_users=total_users,
                metrics=metrics,
                start_time=experiment.start_time or experiment.created_at,
                end_time=experiment.end_time or datetime.utcnow(),
            )
            results.append(result)

        return results


ab_testing_service = ABTestingService()
