from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Data:
    """
    Represents a cache system configuration.

    Attributes
    ----------
    default : str
        A string representing the default cache storage option (e.g., "ram" or "file").
    stores : dict
        A dictionary representing different cache stores. Each key-value pair
        should define a store type and its associated configuration.
    custom : dict
        A dictionary for additional custom properties related to the cache system.
        This field is initialized with an empty dictionary by default.

    Notes
    -----
    The `default` attribute should specify the default cache storage type,
    and the `stores` attribute should hold the configurations for different cache stores.
    The `custom` field allows for extra properties to be dynamically added if needed.
    """

    default: str
    stores: dict
    custom: Dict[str, any] = field(default_factory=dict)
