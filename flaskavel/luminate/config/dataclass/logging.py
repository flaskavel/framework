from dataclasses import dataclass
from typing import Any

@dataclass
class Single:
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
    stream: bool


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
    days : int
        The number of days to retain log files before deletion.
    stream : bool
        Whether to output logs to the console.
    """
    path: str
    level: str
    days: int
    stream: bool


@dataclass
class Chunked:
    """
    Represents a chunked log file configuration.

    Attributes
    ----------
    path : str
        The file path where chunked logs are stored.
    level : str
        The logging level (e.g., 'info', 'error', 'debug').
    lines : int
        The maximum number of lines per log file before creating a new chunk.
    stream : bool
        Whether to output logs to the console.
    """
    path: str
    level: str
    lines: int
    stream: bool


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
    single: Single
    daily: Daily
    chunked: Chunked


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
