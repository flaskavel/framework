from typing import Protocol

class ICache(Protocol):
    """
    A protocol defining the structure of the cache system.

    Attributes
    ----------
    default : str
        A string representing the default cache storage option (e.g., "ram" or "file").
    stores : ICacheStores
        An instance of a class implementing the `ICacheStores` protocol, representing different cache stores.

    Notes
    -----
    The class implementing this protocol must have the `default` and `stores` attributes.
    `default` should be a string indicating which cache storage to use by default,
    and `stores` should be an instance that implements the `ICacheStores` protocol.
    """
    default: str
    stores: dict
