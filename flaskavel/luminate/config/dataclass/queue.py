from dataclasses import dataclass

@dataclass
class Database:
    """
    Represents the configuration for a database-backed queue connection.

    Attributes
    ----------
    driver : str
        The queue driver type (default: 'database').
    connection : Optional[str]
        The database connection name used for storing queued jobs.
    table : str
        The table where queued jobs are stored.
    batching : str
        The table for storing batch job information.
    failed : str
        The table for storing failed jobs.
    queue : str
        The queue name used for processing jobs.
    retry_after : int
        The number of seconds before a job should be retried.
    after_commit : bool
        Whether to process jobs only after a successful database transaction commit.
    """
    connection: str
    table: str
    batching: str
    failed: str
    queue: str
    retry_after: int
    after_commit: bool


@dataclass
class Connections:
    """
    Represents available queue connection configurations.

    Attributes
    ----------
    database : DatabaseQueue
        The configuration for the database-backed queue.
    """

    database: Database

@dataclass
class Queue:
    """
    Represents the overall queue system configuration.

    Attributes
    ----------
    default : str
        The default queue connection to use.
    connections : QueueConnections
        The available queue connection configurations.
    """

    default: str
    connections: Connections
