from typing import Dict, Optional
from dataclasses import dataclass, field

@dataclass
class Sqlite:
    """
    Data class to represent the SQLite database configuration.

    Attributes
    ----------
    driver : str
        The database driver being used, e.g., 'sqlite'.
    url : str
        The URL for connecting to the database.
    database : str
        The path to the SQLite database file.
    prefix : str
        Prefix for table names.
    foreign_key_constraints : bool
        Whether foreign key constraints are enabled.
    busy_timeout : Optional[int]
        The timeout period (in milliseconds) before retrying a locked database.
    journal_mode : Optional[str]
        The journal mode used for transactions.
    synchronous : Optional[str]
        The synchronization level for the database.
    """
    driver: str
    url: str
    database: str
    prefix: str
    foreign_key_constraints: bool
    busy_timeout: Optional[int]
    journal_mode: Optional[str]
    synchronous: Optional[str]

@dataclass
class Mysql:
    """
    Data class to represent the MySQL database configuration.

    Attributes
    ----------
    driver : str
        The database driver being used, e.g., 'mysql'.
    url : str
        The URL for connecting to the database.
    host : str
        The host address for the MySQL server.
    port : str
        The port for connecting to the MySQL server.
    database : str
        The name of the MySQL database.
    username : str
        The username for connecting to the MySQL database.
    password : str
        The password for the MySQL database.
    unix_socket : str
        The path to the Unix socket for MySQL connections (optional).
    charset : str
        The charset used for the connection.
    collation : str
        The collation for the database.
    prefix : str
        Prefix for table names.
    prefix_indexes : bool
        Whether to prefix index names.
    strict : bool
        Whether to enforce strict SQL mode.
    engine : Optional[str]
        The storage engine for the MySQL database (optional).
    """
    driver: str
    url: str
    host: str
    port: str
    database: str
    username: str
    password: str
    unix_socket: str
    charset: str
    collation: str
    prefix: str
    prefix_indexes: bool
    strict: bool
    engine: Optional[str]

@dataclass
class Pgsql:
    """
    Data class to represent the PostgreSQL database configuration.

    Attributes
    ----------
    driver : str
        The database driver being used, e.g., 'pgsql'.
    url : str
        The URL for connecting to the database.
    host : str
        The host address for the PostgreSQL server.
    port : str
        The port for connecting to the PostgreSQL server.
    database : str
        The name of the PostgreSQL database.
    username : str
        The username for connecting to the PostgreSQL database.
    password : str
        The password for the PostgreSQL database.
    charset : str
        The charset used for the connection.
    prefix : str
        Prefix for table names.
    prefix_indexes : bool
        Whether to prefix index names.
    search_path : str
        The schema search path for PostgreSQL.
    sslmode : str
        The SSL mode for the connection.
    """
    driver: str
    url: str
    host: str
    port: str
    database: str
    username: str
    password: str
    charset: str
    prefix: str
    prefix_indexes: bool
    search_path: str
    sslmode: str

@dataclass
class Oracle:
    """
    Data class to represent the Oracle database configuration.

    Attributes
    ----------
    driver : str
        The database driver being used, e.g., 'oracle'.
    dsn : str
        The Data Source Name (DSN) for connecting to the Oracle database.
    host : str
        The host address for the Oracle server.
    port : str
        The port for connecting to the Oracle server.
    username : str
        The username for connecting to the Oracle database.
    password : str
        The password for the Oracle database.
    charset : str
        The charset used for the connection.
    service : str
        The Oracle service name.
    sid : str
        The Oracle System Identifier (SID).
    """
    driver: str
    dsn: str
    host: str
    port: str
    username: str
    password: str
    charset: str
    service: str
    sid: str

@dataclass
class Connections:
    """
    Data class to represent all database connections used by the application.

    Attributes
    ----------
    sqlite : Sqlite
        Configuration for the SQLite database connection.
    mysql : Mysql
        Configuration for the MySQL database connection.
    pgsql : Pgsql
        Configuration for the PostgreSQL database connection.
    oracle : Oracle
        Configuration for the Oracle database connection.
    """
    sqlite: Sqlite
    mysql: Mysql
    pgsql: Pgsql
    oracle: Oracle

@dataclass
class Database:
    """
    Data class to represent the general database configuration.

    Attributes
    ----------
    default : str
        The name of the default database connection to use.
    connections : Connections
        The different database connections available to the application.
    """
    default: str
    connections: Connections

    # Holds additional custom properties, initialized as an empty dictionary
    custom: Dict[str, any] = field(default_factory=dict)