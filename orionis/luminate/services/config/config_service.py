import copy
from typing import Any, Optional
from orionis.contracts.services.config.i_config_service import IConfigService
from orionis.luminate.bootstrap.config_bootstrapper import ConfigBootstrapper

class ConfigService(IConfigService):

    def __init__(self,  config_bootstrapper: ConfigBootstrapper) -> None:
        """
        Initializes the ConfigService with the provided configuration.

        Args:
            config (dict): A dictionary containing configuration settings.
        """
        real_config : dict = config_bootstrapper.get()
        self._config = copy.deepcopy(real_config)

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
        keys = key.split(".")
        section = keys[0]
        sub_keys = keys[1:]

        if section not in self._config:
            self._config[section] = {}

        current = self._config[section]
        for sub_key in sub_keys[:-1]:
            if sub_key not in current:
                current[sub_key] = {}
            current = current[sub_key]

        current[sub_keys[-1]] = value

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
        keys = key.split(".")
        section = keys[0]
        sub_keys = keys[1:]

        if section not in self._config:
            return default

        current = self._config[section]
        for sub_key in sub_keys:
            if sub_key not in current:
                return default
            current = current[sub_key]

        return current