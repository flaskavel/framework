from typing import Any, Optional
from orionis.contracts.facades.config.i_config_facade import IConfig
from orionis.luminate.facades.app_facade import app
from orionis.luminate.services.config.config_service import ConfigService

class Config(IConfig):

    @staticmethod
    def set(key: str, value: Any) -> None:
        """
        Dynamically sets a configuration value using dot notation.

        Parameters
        ----------
        key : str
            The configuration key (e.g., 'app.debug').
        value : Any
            The value to set.
        """
        _config_service_provider : ConfigService = app(ConfigService)
        return _config_service_provider.set(key, value)

    @staticmethod
    def get(key: str, default: Optional[Any] = None) -> Any:
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
        _config_service_provider : ConfigService = app(ConfigService)
        return _config_service_provider.get(key, default)