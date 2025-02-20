from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class Cookie:
    """
    Represents the session cookie configuration.

    Attributes
    ----------
    name : str
        The name of the session cookie.
    path : str
        The path for which the session cookie is available.
    domain : Optional[str]
        The domain where the session cookie is accessible.
    secure : Optional[bool]
        Whether the session cookie should only be sent over HTTPS.
    http_only : bool
        Whether the session cookie is only accessible through HTTP (not JavaScript).
    same_site : str
        The SameSite policy for the session cookie ('lax', 'strict', or 'none').
    """

    name: str = "orionis_session"
    path: str
    domain: Optional[str]
    secure: Optional[bool]
    http_only: bool
    same_site: str


@dataclass
class Session:
    """
    Represents the session management configuration.

    Attributes
    ----------
    driver : str
        The session driver type (e.g., 'file', 'database', 'redis').
    lifetime : int
        The session lifetime in minutes before expiration.
    expire_on_close : bool
        Whether the session expires when the browser is closed.
    encrypt : bool
        Whether session data should be encrypted for additional security.
    files : str
        The file path where session data is stored when using the 'file' driver.
    cookie : SessionCookie
        The configuration settings for the session cookie.
    """

    driver: str
    lifetime: int
    expire_on_close: bool
    encrypt: bool
    files: str
    cookie: Cookie

    # Holds additional custom properties, initialized as an empty dictionary
    custom: Dict[str, any] = field(default_factory=dict)
