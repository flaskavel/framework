from dataclasses import dataclass, field
from datetime import time
from typing import Dict, Union

@dataclass
class Stack:
    """
    Represents a single log file configuration.

    Attributes
    ----------
    path : str
        The file path where the log is stored.
    level : str
        The logging level (e.g., 'info', 'error', 'debug').
    stream : bool
        Whether to output logs to the console.
    """
    path: str
    level: str


@dataclass
class Hourly:
    """
    Represents an hourly log file rotation configuration.

    Attributes
    ----------
    path : str
        The file path where hourly logs are stored.
    level : str
        The logging level (e.g., 'info', 'error', 'debug').
    retention_hours : int
        The number of hours to retain log files before deletion.
    """
    path: str
    level: str
    retention_hours: int


@dataclass
class Daily:
    """
    Represents a daily log file rotation configuration.

    Attributes
    ----------
    path : str
        The file path where daily logs are stored.
    level : str
        The logging level (e.g., 'info', 'error', 'debug').
    retention_days : int
        The number of days to retain log files before deletion.
    at_time : time
        The time of day when the log rotation should occur.
    """
    path: str
    level: str
    retention_days: int
    at: time


@dataclass
class Weekly:
    """
    Represents a weekly log file rotation configuration.

    Attributes
    ----------
    path : str
        The file path where weekly logs are stored.
    level : str
        The logging level (e.g., 'info', 'error', 'debug').
    retention_weeks : int
        The number of weeks to retain log files before deletion.
    """
    path: str
    level: str
    retention_weeks: int


@dataclass
class Monthly:
    """
    Represents a monthly log file rotation configuration.

    Attributes
    ----------
    path : str
        The file path where monthly logs are stored.
    level : str
        The logging level (e.g., 'info', 'error', 'debug').
    retention_months : int
        The number of months to retain log files before deletion.
    """
    path: str
    level: str
    retention_months: int


@dataclass
class Chunked:
    """
    Represents a chunked log file configuration.

    This configuration ensures that log files are split into manageable chunks
    based on size or number of files to prevent excessive file growth.

    Attributes
    ----------
    path : str
        The file path where chunked logs are stored.
    level : str
        The logging level (e.g., 'info', 'error', 'debug').
    max_mb_size : Union[int, str]
        The maximum file size before creating a new chunk.
        Can be an integer (bytes) or a string (e.g., '10MB', '500KB').
    max_files : int
        The maximum number of log files to retain before older files are deleted.
    """
    path: str
    level: str
    mb_size: Union[int, str]
    files: int


@dataclass
class Channels:
    """
    Represents the different logging channels available.

    Attributes
    ----------
    single : Single
        Configuration for single log file storage.
    daily : Daily
        Configuration for daily log file rotation.
    chunked : Chunked
        Configuration for chunked log file storage.
    """
    stack : Stack
    hourly : Hourly
    daily : Daily
    weekly : Weekly
    monthly : Monthly
    chunked : Chunked


@dataclass
class Logging:
    """
    Represents the logging system configuration.

    Attributes
    ----------
    default : str
        The default logging channel to use.
    channels : Channels
        A collection of available logging channels.
    """
    default: str
    channels: Channels

    # Holds additional custom properties, initialized as an empty dictionary
    custom: Dict[str, any] = field(default_factory=dict)
