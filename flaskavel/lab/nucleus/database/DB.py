from flaskavel.lab.catalyst.config import Config
from flaskavel.lab.nucleus.database.database_manager import DatabaseManager
from flaskavel.lab.nucleus.database.db_instance.query_builder import QueryBuilder
from sqlalchemy import Column, Integer, String, Table, MetaData, select, update, delete, and_
from sqlalchemy.orm import sessionmaker
from typing import Any

class DB:
    db_manager = None
    metadata = None
    default_connection = None
    table_instance = None
    query = None
    update_values = None
    delete_filters = None
    columns = []

    @staticmethod
    def initialize():
        """Inicializa la configuración de la base de datos."""
        if DB.db_manager is None:
            config = Config.get('database')  # Configuración de la base de datos
            DB.db_manager = DatabaseManager(config)
            DB.metadata = MetaData()  # Metadatos para las tablas
            DB.default_connection = config.get('default', 'default')  # Conexión predeterminada

    @staticmethod
    def table(table_name: str) -> 'QueryBuilder':
        """Define la tabla que se va a consultar."""
        DB.initialize()  # Inicializa la base de datos si no se ha hecho
        query_builder = QueryBuilder(DB.db_manager, DB.default_connection, DB.metadata)
        return query_builder.table(table_name)

    @staticmethod
    def get() -> Any:
        """Ejecuta la consulta SELECT y obtiene los registros."""
        if DB.query:
            with DB.db_manager.using_connection() as session:
                result = session.execute(DB.query)
                return result.fetchall()
        return []

    @staticmethod
    def execute_update() -> int:
        """Ejecuta la operación UPDATE."""
        if DB.update_values:
            table = Table(DB.update_values['table'], DB.metadata, autoload_with=DB.db_manager._get_engine(DB.default_connection))
            query = update(table).values(DB.update_values['values'])

            # Aplicar los filtros WHERE
            if DB.update_values['filters']:
                for column, value in DB.update_values['filters'].items():
                    query = query.where(getattr(table.c, column) == value)

            with DB.db_manager.using_connection() as session:
                result = session.execute(query)
                session.commit()
                return result.rowcount  # Devuelve el número de filas actualizadas
        return 0

    @staticmethod
    def execute_delete() -> int:
        """Ejecuta la operación DELETE."""
        if DB.delete_filters:
            table = DB.table_instance  # Usar la tabla definida
            query = delete(table)

            # Aplicar los filtros WHERE
            for column, value in DB.delete_filters.items():
                query = query.where(getattr(table.c, column) == value)

            with DB.db_manager.using_connection() as session:
                result = session.execute(query)
                session.commit()
                return result.rowcount  # Devuelve el número de filas eliminadas
        return 0
