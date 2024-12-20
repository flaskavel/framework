from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from flaskavel.lab.catalyst import config
from typing import Callable, Dict, Any

class DatabaseManager:
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the DatabaseManager with a configuration dictionary.

        :param config: Dictionary containing database configurations.
                      Example:
                      {
                          'default': 'sqlite',
                          'connections': {
                              'sqlite': {
                                  'driver': 'sqlite',
                                  'database': 'example.db'
                              },
                              'mysql': {
                                  'driver': 'mysql',
                                  'username': 'root',
                                  'password': '',
                                  'host': 'localhost',
                                  'database': 'test_db'
                              }
                          }
                      }
        """
        self.config = config
        self.engines = {}
        self.sessions = {}
        self.default_connection = config.get('default', 'default')

    def _build_connection_string(self, name: str) -> str:
        """
        Build the SQLAlchemy connection string for the given connection name.

        :param name: Name of the connection
        :return: SQLAlchemy connection string
        """
        config = self.config['connections'].get(name)
        if not config:
            raise ValueError(f"Connection '{name}' is not configured.")

        driver = config['driver']
        if driver == 'sqlite':
            return f"sqlite:///{config['database']}"
        elif driver in ['mysql', 'postgresql', 'mssql', 'oracle']:
            username = config['username']
            password = config.get('password', '')
            host = config['host']
            database = config['database']
            port = config['port']
            return f"{driver}://{username}:{password}@{host}:{port}/{database}"
        else:
            raise ValueError(f"Unsupported driver: {driver}")

    def _get_engine(self, name: str):
        """Get or create an SQLAlchemy engine for the given connection."""
        if name not in self.engines:
            connection_string = self._build_connection_string(name)
            self.engines[name] = create_engine(connection_string)
        return self.engines[name]

    def connection(self, name: str = None):
        """
        Get a scoped session for the given connection.

        :param name: Name of the connection
        :return: SQLAlchemy session
        """
        name = name or self.default_connection

        if name not in self.sessions:
            engine = self._get_engine(name)
            session_factory = sessionmaker(bind=engine)
            self.sessions[name] = scoped_session(session_factory)
        return self.sessions[name]

    def reconnect(self, name: str = None):
        """
        Reconnect to the database.

        :param name: Name of the connection
        """
        name = name or self.default_connection

        if name in self.engines:
            del self.engines[name]
        if name in self.sessions:
            self.sessions[name].remove()
            del self.sessions[name]

    def disconnect(self, name: str = None):
        """
        Disconnect from the database.

        :param name: Name of the connection
        """
        name = name or self.default_connection

        if name in self.sessions:
            self.sessions[name].remove()
            del self.sessions[name]

    @contextmanager
    def using_connection(self, name: str = None):
        """
        Context manager for using a specific database connection.

        :param name: Name of the connection
        """
        session = self.connection(name)
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.remove()

    def set_default_connection(self, name: str):
        """Set the default connection name."""
        if name not in self.config['connections']:
            raise ValueError(f"Connection '{name}' is not configured.")
        self.default_connection = name