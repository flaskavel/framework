from abc import ABC
from dataclasses import dataclass

@dataclass
class EmptyData:
    """
    A placeholder dataclass that can be used as a default or empty configuration.
    This class doesn't have any fields or data, but serves as a default value
    for the 'config' attribute in classes implementing IConfig.
    """
    pass

class IConfig(ABC):
    """
    An abstract base class that defines an interface for classes that must have
    a `config` attribute.

    The subclass is required to implement the `config` attribute, which should be
    a dataclass instance representing the configuration data.

    Attributes
    ----------
    config : object
        A dataclass instance representing the configuration.
    """

    config = EmptyData()
