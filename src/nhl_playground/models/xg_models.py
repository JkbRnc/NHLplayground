from nhl_playground.models.base import BaseModel, ModelType


class XGBaseModel(BaseModel):
    """xG model base class."""

    def __init__(self) -> None:
        """Initialize XG model."""
        self.model_type = ModelType.XG
        super().__init__()
