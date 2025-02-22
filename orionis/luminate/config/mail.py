from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class Smtp:
    """
    Represents SMTP (Simple Mail Transfer Protocol) configuration settings.

    Attributes
    ----------
    url : str
        The full URL for the SMTP service.
    host : str
        The hostname of the SMTP server (e.g., 'smtp.example.com').
    port : int
        The port number used for SMTP communication (e.g., 465, 587).
    encryption : str
        The encryption type used for secure communication (e.g., 'SSL', 'TLS', 'None').
    username : str
        The username for authentication with the SMTP server.
    password : str
        The password for authentication with the SMTP server.
    timeout : Optional[int], default=None
        The connection timeout duration in seconds. If None, defaults to the system setting.
    """

    url: str
    host: str
    port: int
    encryption: str
    username: str
    password: str
    timeout: Optional[int] = None


@dataclass
class File:
    """
    Represents email file-based storage configuration.

    Attributes
    ----------
    path : str
        The file path where outgoing emails are stored instead of being sent.
    """

    path: str


@dataclass
class Mailers:
    """
    Represents the available mail transport configurations.

    Attributes
    ----------
    smtp : Smtp
        The SMTP configuration used for sending emails.
    file : File
        The file-based mail transport configuration (used for local development/testing).
    """

    smtp: Smtp
    file: File


@dataclass
class Mail:
    """
    Represents the overall mail configuration.

    Attributes
    ----------
    default : str
        The default mailer transport to use (e.g., 'smtp', 'file').
    mailers : Mailers
        The available mail transport configurations.
    """

    default: str
    mailers: Mailers

    # Holds additional custom properties, initialized as an empty dictionary
    custom: Dict[str, any] = field(default_factory=dict)
