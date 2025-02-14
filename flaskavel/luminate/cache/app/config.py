from typing import Dict, Any

class CacheConfig:
    """
    Singleton class for managing application configuration caching.

    This class ensures that configuration sections are registered only once
    and provides methods to register, unregister, and retrieve configurations.

    Attributes
    ----------
    _instance : CacheConfig
        A private class attribute that holds the singleton instance.
    config : dict
        A dictionary storing registered configuration sections.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Ensures a single instance of CacheConfig (Singleton Pattern).

        Returns
        -------
        CacheConfig
            The singleton instance of the class.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = {}
        return cls._instance

    def register(self, section: str, data: Dict[str, Any]) -> None:
        """
        Registers a configuration section.

        Parameters
        ----------
        section : str
            The name of the configuration section to register.
        data : dict
            The configuration data associated with the section.

        Raises
        ------
        ValueError
            If the section is already registered.
        """
        if section in self.config:
            raise ValueError(f"Configuration section '{section}' is already registered.")

        self.config[section] = data

    def unregister(self, section: str) -> None:
        """
        Unregisters a previously registered configuration section.

        Parameters
        ----------
        section : str
            The name of the configuration section to remove.

        Raises
        ------
        KeyError
            If the section is not found in the registered configurations.
        """
        if section not in self.config:
            raise KeyError(f"Configuration section '{section}' is not registered.")

        del self.config[section]

    def get(self, section: str) -> Dict[str, Any]:
        """
        Retrieves the configuration for a specific section.

        Parameters
        ----------
        section : str
            The name of the configuration section to retrieve.

        Returns
        -------
        dict
            The configuration data for the specified section.

        Raises
        ------
        KeyError
            If the requested section is not found.
        """
        if section not in self.config:
            raise KeyError(f"Configuration section '{section}' is not registered.")

        return self.config[section]
