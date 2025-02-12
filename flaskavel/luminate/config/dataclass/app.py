from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Data:
    """
    Represents the application configuration.

    Attributes
    ----------
    name : str
        The name of the application.
    debug : bool
        Indicates whether debugging is enabled.
    bytecode : bool
        Whether bytecode caching is enabled.
    timezone : str
        The timezone for the application.
    url : str
        The base URL of the application.
    port : int
        The port number to run the application.
    cipher : str
        The encryption cipher to be used.
    key : str
        The encryption key.
    custom : dict
        A dictionary to store any additional custom properties for the application.
        This field is initialized with an empty dictionary by default.
    """

    # Application properties (e.g., name, debug status, etc.)
    name: str
    debug: bool
    bytecode: bool
    timezone: str
    url: str
    port: int
    cipher: str
    key: str

    # Custom dictionary to hold dynamic or extra properties, initialized as an empty dict
    custom: Dict[str, any] = field(default_factory=dict)
