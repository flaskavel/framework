from pyparsing import Any
from sqlalchemy import Table, MetaData, select, and_
from flaskavel.lab.nucleus.database.database_manager import DatabaseManager

class QueryBuilder:
    def __init__(self, db_manager: DatabaseManager, default_connection: str, metadata: MetaData):
        self.db_manager = db_manager
        self.default_connection = default_connection
        self.metadata = metadata
        self.table_instance = None
        self.query = None

    def table(self, table_name: str) -> 'QueryBuilder':
        """Define la tabla que se va a consultar."""
        engine = self.db_manager._get_engine(self.default_connection)
        self.table_instance = Table(table_name, self.metadata, autoload_with=engine)
        self.query = select(self.table_instance)
        return self

    def where(self, filters: dict) -> 'QueryBuilder':
        """Añade cláusulas WHERE a la consulta."""
        if self.query:
            conditions = [getattr(self.table_instance.c, column) == value for column, value in filters.items()]
            self.query = self.query.where(and_(*conditions))
        return self

    def select(self, columns: list = []) -> 'QueryBuilder':
        """Define las columnas a seleccionar."""
        if columns:
            # Pasar las columnas como parámetros posicionales, no como una lista
            self.query = self.query.with_only_columns(*[getattr(self.table_instance.c, column) for column in columns])
        else:
            # Si no se pasan columnas, seleccionar todo (*)
            self.query = self.query.with_only_columns(self.table_instance)  # Selección por defecto (todas las columnas)
        return self

    def get(self) -> Any:
        """Ejecuta la consulta SELECT y obtiene los registros."""
        with self.db_manager.using_connection() as session:
            result = session.execute(self.query)

            # Convertir cada fila (row) en un diccionario utilizando _mapping
            results_list = [dict(row._mapping) for row in result]
            return results_list
