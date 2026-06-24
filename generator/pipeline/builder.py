from config.models import PipelineConfig
from generator.pipeline.base import Pipeline
from generator.pipeline.steps.duplicate import DuplicateStep
from generator.pipeline.steps.field_corrupt import FieldCorruptionStep
from generator.pipeline.steps.nullify import NullifyStep
from generator.pipeline.steps.user_legacy import UserLegacyStep


def build_pipeline(pipeline_config: PipelineConfig) -> Pipeline:
    steps = [
        FieldCorruptionStep(pipeline_config.field_corrupt_rates),
        UserLegacyStep(pipeline_config.legacy_rate),
        NullifyStep(pipeline_config.null_rates),
        DuplicateStep(pipeline_config.duplication_rate)
    ]
    return Pipeline(steps)
