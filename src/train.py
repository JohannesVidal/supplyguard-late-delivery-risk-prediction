"""
Model training utilities for the SupplyGuard project.
"""

from sklearn.pipeline import Pipeline


def build_model_pipeline(preprocessor, model) -> Pipeline:
    """Build a full sklearn pipeline with preprocessing and model."""
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )
