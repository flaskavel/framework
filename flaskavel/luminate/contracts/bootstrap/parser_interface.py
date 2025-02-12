from abc import ABC, abstractmethod
from typing import Any

class IParser(ABC):
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

    @abstractmethod
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
        pass

