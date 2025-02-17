from dataclasses import dataclass
from typing import Any, Union

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

    This configuration ensures that log files are split into manageable chunks
    based on size or number of files to prevent excessive file growth.

    Attributes
    ----------
    path : str
        The file path where chunked logs are stored.
    level : str
        The logging level (e.g., 'info', 'error', 'debug').
    max_size : Union[int, str]
        The maximum file size before creating a new chunk.
        Can be an integer (bytes) or a string (e.g., '10MB', '500KB').
    max_files : int
        The maximum number of log files to retain before older files are deleted.
    stream : bool
        Whether to output logs to the console.
    """

    path: str
    level: str
    max_size: Union[int, str]  # Supports both numeric and formatted string sizes ('10MB')
    max_files: int  # Ensures only a certain number of log files are kept
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
