from abc import ABC, abstractmethod
from typing import Any, Optional

class IConfigService(ABC):

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """
        Dynamically sets a configuration value using dot notation.

        Parameters
        ----------
        key : str
            The configuration key (e.g., 'app.debug').
        value : Any
            The value to set.
        """
        pass

    @abstractmethod
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Retrieves a configuration value using dot notation.

        Parameters
        ----------
        key : str
            The configuration key (e.g., 'app.debug').
        default : Optional[Any]
            The default value to return if the key is not found.

        Returns
        -------
        Any
            The configuration value or the default value if the key is not found.
        """
        pass