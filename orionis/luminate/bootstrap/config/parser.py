from typing import Any
from dataclasses import asdict
from orionis.luminate.contracts.bootstrap.parser_interface import IParser

class Parser(IParser):
    """
    A class responsible for parsing configuration objects into dictionaries.

    This class implements the `IParser` interface and provides a method
    to convert configuration instances into a dictionary format.

    Methods
    -------
    toDict(instance: Any) -> dict
        Converts the `config` attribute of an instance into a dictionary.
    """

    @staticmethod
    def toDict(instance: Any) -> dict:
        """
        Converts the `config` attribute of a given instance into a dictionary.

        This method uses `asdict()` to transform a dataclass-based configuration
        into a dictionary, ensuring that all attributes are properly serialized.

        Parameters
        ----------
        instance : Any
            The object containing a `config` attribute to be converted.

        Returns
        -------
        dict
            A dictionary representation of the `config` attribute.

        Raises
        ------
        AttributeError
            If the provided instance does not have a `config` attribute.
        TypeError
            If the `config` attribute cannot be converted to a dictionary.
        """
        try:
            # Check if instance is a dictionary
            if isinstance(instance.config, dict):
                return instance
            # Check if instance is a dataclass
            elif hasattr(instance.config, '__dataclass_fields__'):
                return asdict(instance.config)
        except AttributeError as e:
            raise AttributeError("The provided instance does not have a 'config' attribute.") from e
        except TypeError as e:
            raise TypeError(f"Error: The 'config' attribute could not be converted to a dictionary. {str(e)}")
