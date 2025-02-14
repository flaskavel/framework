from dataclasses import dataclass, field
from typing import Dict

@dataclass
class App:
    """
    Represents the application's core configuration.

    This class defines the essential settings for the application, including
    its name, debugging mode, encryption settings, and server-related properties.

    Attributes
    ----------
    name : str
        The name of the application, used in logs, UI elements, and notifications.
    debug : bool
        Determines whether debugging mode is enabled. Should be `False` in production.
    bytecode : bool
        Indicates whether Python bytecode caching (.pyc files) is enabled.
    timezone : str
        The default timezone for the application, used for logging and scheduled tasks.
    url : str
        The base URL or host address where the application runs.
    port : int
        The port number the application listens on.
    workers : int
        The number of worker processes handling requests (affects performance).
    reload : bool
        Enables automatic server reloading when code changes (useful for development).
    cipher : str
        The encryption algorithm used for secure data handling (e.g., "AES-256-GCM").
    key : str
        The encryption key used for cryptographic operations.
    custom : dict
        A dictionary for storing additional custom properties. Defaults to an empty dictionary.
    """

    name: str
    debug: bool
    bytecode: bool
    timezone: str
    url: str
    port: int
    workers: int
    reload: bool
    cipher: str
    key: str

    # Holds additional custom properties, initialized as an empty dictionary
    custom: Dict[str, any] = field(default_factory=dict)
