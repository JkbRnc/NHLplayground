from typing import Any, ClassVar

from nhl_playground.models.base_model import BaseModel, ModelType
from nhl_playground.models.xg_models import XGBaseModel


class ModelFactory:
    """Factory class for creating models."""

    MODEL_MAPPING: ClassVar[dict] = {ModelType.XG: XGBaseModel}

    @classmethod
    def create_model(self, model_type: ModelType, specified_model: object, **model_params: dict[str, Any]) -> BaseModel:
        """Creates a model based on the given model type."""
        if model_type not in self.MODEL_MAPPING:
            raise ValueError(f"Model type {model_type} is not allowed.")
        model = self.MODEL_MAPPING[model_type]()
        model.set_model(specified_model)
        model.initialize_model(**model_params)

        return model
