from config.models import PipelineConfig
from generator.pipeline.base import Pipeline
from generator.pipeline.steps.duplicate import DuplicateStep
from generator.pipeline.steps.field_corrupt import FieldCaseCorruptionStep
from generator.pipeline.steps.trailing_spaces import TrailingSpacesCorruptionStep
from generator.pipeline.steps.nullify import NullifyStep
from generator.pipeline.steps.user_legacy import AlphaUserLegacyStep, BetaUserLegacyStep


def build_pipeline(pipeline_config: PipelineConfig) -> Pipeline:
    steps = [
        FieldCaseCorruptionStep(pipeline_config.field_case_corrupt_rates),
        AlphaUserLegacyStep(pipeline_config.legacy_rate),
        BetaUserLegacyStep(pipeline_config.legacy_rate),
        NullifyStep(pipeline_config.null_rates),
    ]
    if pipeline_config.trailing_spaces_corrupt_rates:
        steps.append(TrailingSpacesCorruptionStep(pipeline_config.trailing_spaces_corrupt_rates))

    if pipeline_config.duplication_rate > 0:
        steps.append(DuplicateStep(pipeline_config.duplication_rate))

    return Pipeline(steps)
