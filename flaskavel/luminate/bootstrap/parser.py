from typing import Any
from dataclasses import asdict
from flaskavel.luminate.contracts.config.config_interface import IConfig
from flaskavel.luminate.contracts.bootstrap.parser_interface import IParser

class Parser(IParser):
    """
    A class responsible for parsing an instance's configuration and outputting it as a dictionary.

    This class uses Python's `dataclasses.asdict()` method to convert an instance's `config` attribute to a dictionary.

    Methods
    -------
    parse(instance: Any) -> dict
        Takes an instance with a `config` attribute and returns its dictionary representation.

    Notes
    -----
    - This method expects the instance to have a `config` attribute that is a dataclass or any object that supports `asdict()`.
    - The `asdict()` function will recursively convert dataclass fields into a dictionary format.
    - If `instance.config` is not a dataclass, this could raise an exception depending on the type.
    """

    def dataClass(self, instance: Any) -> dict:
        """
        Converts the `config` attribute of the provided instance to a dictionary and returns it.

        Parameters
        ----------
        instance : Any
            The instance to parse. It is expected that the instance has a `config` attribute
            that is a dataclass or any object that supports `asdict()`.

        Returns
        -------
        dict
            The dictionary representation of the `config` attribute.

        Raises
        ------
        AttributeError
            If the `instance` does not have a `config` attribute.
        TypeError
            If the `instance.config` is not a valid dataclass or object that supports `asdict()`.
        """
        try:

            # Validate inheritance from 'IConfig'
            if not issubclass(instance, IConfig):
                raise TypeError(f"Class {instance.__name__} must inherit from 'IConfig'.")

            # Check if the instance has a 'config' attribute and convert it to a dictionary
            if not hasattr(instance, 'config'):
                raise AttributeError(f"Error: The provided instance does not have a 'config' attribute.")

            # Convert the 'config' attribute to a dictionary using asdict()
            return asdict(instance.config)

        except AttributeError as e:
            # Handle the case where 'config' attribute is missing
            raise e

        except TypeError as e:
            # Handle the case where 'config' attribute cannot be converted to a dictionary
            raise TypeError(f"Error: The 'config' attribute could not be converted to a dictionary. {str(e)}")

