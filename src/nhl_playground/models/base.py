from abc import ABC, abstractmethod
from enum import StrEnum

from pandas import DataFrame


class ModelType(StrEnum):
    """Enumeration of model types."""

    XG = "xg"


class BaseModel(ABC):
    """Abstract model base class."""

    _model_type: ModelType

    def __init__(self) -> None:
        """Model constructor."""
        self._trained = False

    @property
    def trained(self) -> bool:
        """Getter for trained flag."""
        return self._trained

    @property
    def model_type(self) -> str:
        """Getter for model type."""
        return self._model_type

    @model_type.setter
    def model_type(self, model_type: ModelType) -> None:
        if model_type == self.model_type:
            return

        self._trained = False
        self._model_type = model_type

    @abstractmethod
    def load_model(self, path: str) -> None:
        """Loads model."""
        raise NotImplementedError

    @abstractmethod
    def fit(self, data: DataFrame) -> None:
        """Fits model."""
        raise NotImplementedError

    @abstractmethod
    def predict(self, data: DataFrame) -> DataFrame:
        """Predicts using the model."""
        raise NotImplementedError

    @abstractmethod
    def set_model(self, model: object) -> None:
        """Sets model."""
        raise NotImplementedError

    @abstractmethod
    def initialize_model(**kwargs) -> None:
        """Initializes model."""
        raise NotImplementedError
