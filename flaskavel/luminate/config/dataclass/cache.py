from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class File:
    """
    Represents a file storage path.

    Attributes
    ----------
    path : str
        The file path used for caching.
    """
    path: str

@dataclass
class Stores:
    """
    Defines available cache stores.

    Attributes
    ----------
    file : File
        An instance of `File` representing file-based cache storage.
    """
    file: File

@dataclass
class Cache:
    """
    Configuration for a cache system.

    Attributes
    ----------
    default : str
        The default cache storage type (e.g., "ram" or "file").
    stores : Stores
        An instance of `Stores` containing cache storage configurations.
    custom : Dict[str, Any], optional
        A dictionary containing additional custom properties for cache configuration.
        Defaults to an empty dictionary.

    Notes
    -----
    - The `default` attribute defines the main cache type.
    - The `stores` attribute holds configurations for different cache stores.
    - The `custom` attribute allows for dynamic additional properties if needed.
    """
    default: str
    stores: Stores = field(default_factory=lambda: Stores(File("")))
    custom: Dict[str, Any] = field(default_factory=dict)
