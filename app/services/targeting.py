from typing import List, Dict, Any, Optional
from datetime import datetime
import hashlib
import json
from ..core.redis import get_redis
from ..models.targeting import (
    TargetingRule,
    UserSegment,
    TargetingCondition,
    TargetingOperator,
    TargetingEvaluation,
)


class TargetingService:
    def __init__(self):
        self.redis = None

    async def _get_redis(self):
        if self.redis is None:
            self.redis = await get_redis()
        return self.redis

    def _evaluate_condition(
        self, condition: TargetingCondition, context: Dict[str, Any]
    ) -> bool:
        if condition.attribute not in context:
            return False

        value = context[condition.attribute]
        target_value = condition.value

        if condition.operator == TargetingOperator.EQUALS:
            return value == target_value
        elif condition.operator == TargetingOperator.NOT_EQUALS:
            return value != target_value
        elif condition.operator == TargetingOperator.CONTAINS:
            return (
                target_value in value
                if isinstance(value, (list, str))
                else False
            )
        elif condition.operator == TargetingOperator.NOT_CONTAINS:
            return (
                target_value not in value
                if isinstance(value, (list, str))
                else True
            )
        elif condition.operator == TargetingOperator.GREATER_THAN:
            return (
                value > target_value
                if isinstance(value, (int, float))
                else False
            )
        elif condition.operator == TargetingOperator.LESS_THAN:
            return (
                value < target_value
                if isinstance(value, (int, float))
                else False
            )
        elif condition.operator == TargetingOperator.IN:
            return (
                value in target_value
                if isinstance(target_value, list)
                else False
            )
        elif condition.operator == TargetingOperator.NOT_IN:
            return (
                value not in target_value
                if isinstance(target_value, list)
                else False
            )
        elif condition.operator == TargetingOperator.BETWEEN:
            if not isinstance(target_value, list) or len(target_value) != 2:
                return False
            return (
                target_value[0] <= value <= target_value[1]
                if isinstance(value, (int, float))
                else False
            )
        elif condition.operator == TargetingOperator.NOT_BETWEEN:
            if not isinstance(target_value, list) or len(target_value) != 2:
                return False
            return (
                not (target_value[0] <= value <= target_value[1])
                if isinstance(value, (int, float))
                else True
            )
        return False

    def _evaluate_rule(
        self, rule: TargetingRule, context: Dict[str, Any]
    ) -> TargetingEvaluation:
        matched_conditions = []
        unmatched_conditions = []

        for condition in rule.conditions:
            if self._evaluate_condition(condition, context):
                matched_conditions.append(condition.attribute)
            else:
                unmatched_conditions.append(condition.attribute)

        # Check time constraints
        now = datetime.utcnow()
        if rule.start_time and now < rule.start_time:
            return TargetingEvaluation(
                rule_id=rule.name,
                result=False,
                matched_conditions=[],
                unmatched_conditions=[c.attribute for c in rule.conditions],
                evaluation_time=now,
            )
        if rule.end_time and now > rule.end_time:
            return TargetingEvaluation(
                rule_id=rule.name,
                result=False,
                matched_conditions=[],
                unmatched_conditions=[c.attribute for c in rule.conditions],
                evaluation_time=now,
            )

        # Check percentage if specified
        if rule.percentage is not None:
            context_hash = hashlib.md5(
                json.dumps(context, sort_keys=True).encode()
            ).hexdigest()
            hash_int = int(context_hash, 16)
            percentage_match = (hash_int % 100) < rule.percentage
            if not percentage_match:
                return TargetingEvaluation(
                    rule_id=rule.name,
                    result=False,
                    matched_conditions=[],
                    unmatched_conditions=[c.attribute for c in rule.conditions],
                    evaluation_time=now,
                )

        return TargetingEvaluation(
            rule_id=rule.name,
            result=len(matched_conditions) == len(rule.conditions),
            matched_conditions=matched_conditions,
            unmatched_conditions=unmatched_conditions,
            evaluation_time=now,
        )

    async def evaluate_rules(
        self, rules: List[TargetingRule], context: Dict[str, Any]
    ) -> List[TargetingEvaluation]:
        return [self._evaluate_rule(rule, context) for rule in rules]

    async def create_rule(self, rule: TargetingRule) -> TargetingRule:
        redis = await self._get_redis()
        rule_dict = rule.model_dump()
        await redis.hset(f"rule:{rule.name}", mapping=rule_dict)
        await redis.sadd("rules", rule.name)
        return rule

    async def get_rule(self, name: str) -> Optional[TargetingRule]:
        redis = await self._get_redis()
        rule_data = await redis.hgetall(f"rule:{name}")
        if not rule_data:
            return None
        return TargetingRule(**rule_data)

    async def update_rule(
        self, name: str, rule: TargetingRule
    ) -> Optional[TargetingRule]:
        redis = await self._get_redis()
        existing_rule = await self.get_rule(name)
        if not existing_rule:
            return None

        rule_dict = rule.model_dump()
        rule_dict["updated_at"] = datetime.utcnow()
        await redis.hset(f"rule:{name}", mapping=rule_dict)
        return TargetingRule(**rule_dict)

    async def delete_rule(self, name: str) -> bool:
        redis = await self._get_redis()
        if not await redis.exists(f"rule:{name}"):
            return False
        await redis.delete(f"rule:{name}")
        await redis.srem("rules", name)
        return True

    async def list_rules(self) -> List[TargetingRule]:
        redis = await self._get_redis()
        rule_names = await redis.smembers("rules")
        rules = []
        for name in rule_names:
            rule_data = await redis.hgetall(f"rule:{name}")
            if rule_data:
                rules.append(TargetingRule(**rule_data))
        return rules

    async def create_segment(self, segment: UserSegment) -> UserSegment:
        redis = await self._get_redis()
        segment_dict = segment.model_dump()
        await redis.hset(f"segment:{segment.name}", mapping=segment_dict)
        await redis.sadd("segments", segment.name)
        return segment

    async def get_segment(self, name: str) -> Optional[UserSegment]:
        redis = await self._get_redis()
        segment_data = await redis.hgetall(f"segment:{name}")
        if not segment_data:
            return None
        return UserSegment(**segment_data)

    async def update_segment(
        self, name: str, segment: UserSegment
    ) -> Optional[UserSegment]:
        redis = await self._get_redis()
        existing_segment = await self.get_segment(name)
        if not existing_segment:
            return None

        segment_dict = segment.model_dump()
        segment_dict["updated_at"] = datetime.utcnow()
        await redis.hset(f"segment:{name}", mapping=segment_dict)
        return UserSegment(**segment_dict)

    async def delete_segment(self, name: str) -> bool:
        redis = await self._get_redis()
        if not await redis.exists(f"segment:{name}"):
            return False
        await redis.delete(f"segment:{name}")
        await redis.srem("segments", name)
        return True

    async def list_segments(self) -> List[UserSegment]:
        redis = await self._get_redis()
        segment_names = await redis.smembers("segments")
        segments = []
        for name in segment_names:
            segment_data = await redis.hgetall(f"segment:{name}")
            if segment_data:
                segments.append(UserSegment(**segment_data))
        return segments


targeting_service = TargetingService()
