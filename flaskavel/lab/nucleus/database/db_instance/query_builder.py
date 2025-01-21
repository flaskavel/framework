from pyparsing import Any
from sqlalchemy import Table, MetaData, delete, insert, select, and_, update, distinct, desc, asc, func
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

    def where(self, column: str, value: Any, operator: str = "=") -> 'QueryBuilder':
        """
        Añade una cláusula WHERE a la consulta.
        Soporta valores únicos o múltiples valores (para 'WHERE IN').
        """
        # Verificar que la tabla y la consulta estén correctamente inicializadas
        if self.table_instance is None:
            raise ValueError("Tabla no inicializada. Usa el método 'table' primero.")

        # Obtener la columna de la tabla
        column_expr = getattr(self.table_instance.c, column)

        # Si el valor es un iterable (list, tuple, set), se utiliza "IN"
        if isinstance(value, (list, set, tuple)):
            if len(value) == 1:  # Un solo elemento -> Comparación normal
                condition = column_expr == list(value)[0]
            elif len(value) > 1:  # Múltiples elementos -> IN
                condition = column_expr.in_(value)
            else:  # Vacío -> Error
                raise ValueError(f"The iterable for column '{column}' in 'WHERE IN' cannot be empty.")
        else:
            # Si se pasa un operador, se aplica
            if operator == "=":
                condition = column_expr == value
            elif operator == "!=":
                condition = column_expr != value
            elif operator == ">":
                condition = column_expr > value
            elif operator == "<":
                condition = column_expr < value
            elif operator.lower() == "like":
                condition = column_expr.like(value)
            else:
                raise ValueError(f"Operador '{operator}' no soportado.")

        # Añadir la condición al WHERE
        self.query = self.query.where(condition)

        return self

    def select(self, *columns: str) -> 'QueryBuilder':
        """Define las columnas a seleccionar."""
        if columns:
            # Pasar las columnas como parámetros posicionales
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

    def first(self) -> Any:
        """Ejecuta la consulta SELECT y obtiene el primer registro encontrado."""
        with self.db_manager.using_connection() as session:
            result = session.execute(self.query)

            # Convertir cada fila (row) en un diccionario utilizando _mapping
            results_list = [dict(row._mapping) for row in result]

            # Retornar el primer registro o None si no hay resultados
            if results_list:
                return results_list[0]  # Primer elemento de la lista
            return None

    def create(self, data: dict | list) -> Any:
        """Inserta un nuevo registro o múltiples registros en la tabla usando bulk insert cuando sea necesario."""

        if self.table_instance is None:
            raise ValueError("Tabla no inicializada. Usa el método 'table' primero.")

        # Si 'data' es un solo diccionario, lo convertimos a una lista para tratarlo uniformemente
        if isinstance(data, dict):
            data = [data]

        # Si 'data' tiene más de un registro, usamos una inserción múltiple con 'insert().values()'
        if len(data) > 1:
            # Convertir los datos a un formato que sea adecuado para insertarlos en bloque
            # Excluir 'id' de los datos a insertar
            insert_data = [
                {column.name: record.get(column.name) for column in self.table_instance.columns if column.name != 'id'}
                for record in data
            ]

            with self.db_manager.using_connection() as session:  # Usar la conexión
                session.execute(insert(self.table_instance).values(insert_data))  # Inserción en bloque
                session.commit()
                return len(data)  # Devolvemos el número de registros insertados

        # Si es solo un registro, hacemos la inserción tradicional
        insert_data = {column.name: data[0].get(column.name) for column in self.table_instance.columns if column.name != 'id'}  # Excluir 'id'

        stmt = insert(self.table_instance).values(insert_data)  # No pasar 'id'

        with self.db_manager.using_connection() as session:
            result = session.execute(stmt)
            session.commit()

            # Aquí no es necesario recuperar el id manualmente, ya que lo genera automáticamente la base de datos.
            return result.rowcount  # Devuelve la cantidad de registros insertados


    def update(self, where_conditions: dict, data: dict) -> Any:
        """Actualiza los registros de la tabla que cumplen con las condiciones WHERE."""
        if self.table_instance is None:
            raise ValueError("Tabla no inicializada. Usa el método 'table' primero.")

        # Verificar si where_conditions es un diccionario
        if not isinstance(where_conditions, dict):
            raise ValueError("where_conditions debe ser un diccionario.")

        # Inicializar una lista de condiciones
        conditions = []

        # Iterar sobre las condiciones 'where_conditions' y construir dinámicamente las condiciones WHERE
        for column, value in where_conditions.items():
            condition = getattr(self.table_instance.c, column) == value
            conditions.append(condition)

        # Aplicar todas las condiciones WHERE usando 'and_' para combinarlas
        where_clause = and_(*conditions)

        # Crear la sentencia de actualización
        stmt = update(self.table_instance).where(where_clause).values(data)

        with self.db_manager.using_connection() as session:
            result = session.execute(stmt)
            session.commit()
            return result.rowcount  # Devuelve la cantidad de registros actualizados

    def delete(self, column: str, value: any) -> Any:
        """Elimina los registros de la tabla que cumplen con las condiciones WHERE."""
        if self.table_instance is None:
            raise ValueError("Tabla no inicializada. Usa el método 'table' primero.")

        conditions = []

        if isinstance(value, (list, set, tuple)):
            if len(value) == 1:  # Un solo elemento -> Comparación normal
                condition = getattr(self.table_instance.c, column) == list(value)[0]
            elif len(value) > 1:  # Múltiples elementos -> IN
                condition = getattr(self.table_instance.c, column).in_(value)
            else:  # Vacío -> Error
                raise ValueError(f"The iterable for column '{column}' in 'WHERE IN' cannot be empty.")
            conditions.append(condition)
        else:
            condition = getattr(self.table_instance.c, column) == value
            conditions.append(condition)

        if conditions:
            where_clause = and_(*conditions)
            stmt = delete(self.table_instance).where(where_clause)

            with self.db_manager.using_connection() as session:
                result = session.execute(stmt)
                session.commit()
                return result.rowcount

    def update_or_create(self, where_conditions: dict, data: dict) -> Any:
        """
        Busca el primer registro que cumpla con las condiciones WHERE.
        Si se encuentra, actualiza el registro con los datos proporcionados.
        Si no se encuentra, crea un nuevo registro con los datos proporcionados.
        """
        if self.table_instance is None:
            raise ValueError("Tabla no inicializada. Usa el método 'table' primero.")

        # Aplicar las condiciones WHERE a la consulta
        for column, value in where_conditions.items():
            self.where(column, value)

        # Buscar el primer registro que cumpla con las condiciones WHERE
        existing_record = self.first()  # Utiliza 'first' directamente en lugar de 'where(...).first()'

        if existing_record:
            # Si se encuentra el registro, realizar la actualización
            return self.update(where_conditions, data)
        else:
            # Si no se encuentra el registro, realizar la inserción
            return self.create(data)

    def update_or_create_masive(self, data_list: list) -> Any:
        """
        Para cada elemento en data_list, busca si el registro existe según las condiciones 'where_conditions'.
        Si existe, actualiza el registro, si no, lo crea.
        Cada elemento de 'data_list' puede tener sus propias condiciones de búsqueda.
        """
        if self.table_instance is None:
            raise ValueError("Tabla no inicializada. Usa el método 'table' primero.")

        updated_count = 0  # Contador para saber cuántos registros se actualizaron
        inserted_count = 0  # Contador para saber cuántos registros se insertaron

        for data in data_list:
            # Verificar que cada diccionario tenga 'where_conditions' y 'data'
            where_conditions = data.get('where_conditions')
            if not where_conditions:
                raise ValueError("Cada elemento de data_list debe contener 'where_conditions'.")

            data_to_insert_or_update = {key: value for key, value in data.items() if key != 'where_conditions'}

            # Aplicar las condiciones WHERE a la consulta para este registro
            self.query = select(self.table_instance).where(
                and_(*[getattr(self.table_instance.c, column) == value for column, value in where_conditions.items()])
            )

            # Buscar el primer registro que cumpla con las condiciones WHERE
            existing_record = self.first()

            if existing_record:
                # Si se encuentra el registro, realizar la actualización
                self.update(where_conditions, data_to_insert_or_update)
                updated_count += 1
            else:
                # Si no se encuentra el registro, realizar la inserción
                self.create(data_to_insert_or_update)
                inserted_count += 1

        return {"updated": updated_count, "inserted": inserted_count}

    def order_by(self, column: str, order: str = None) -> 'QueryBuilder':
        """Agrega una cláusula ORDER BY a la consulta."""

        # Si 'order' no es especificado, se asume ascendente
        if order == 'desc':
            order_clause = desc(getattr(self.table_instance.c, column))
        else:
            order_clause = asc(getattr(self.table_instance.c, column))

        # Agregar la cláusula ORDER BY a la consulta
        self.query = self.query.order_by(order_clause)

        return self

    def distinct(self, *columns: str) -> 'QueryBuilder':
        """Aplica DISTINCT a las columnas especificadas."""
        if columns:
            # Si se pasan columnas, aplicar DISTINCT solo a esas columnas
            distinct_clause = [getattr(self.table_instance.c, column) for column in columns]
            self.query = self.query.distinct(*distinct_clause)
        else:
            # Si no se pasan columnas, aplicar DISTINCT a toda la consulta
            self.query = self.query.distinct()
        return self

    def group_by(self, *columns: str) -> 'QueryBuilder':
        """Agrega una cláusula GROUP BY a la consulta."""
        # Si no se pasan columnas, lanzamos un error
        if not columns:
            raise ValueError("Debe proporcionar al menos una columna para el GROUP BY.")

        # Aplicar GROUP BY a las columnas especificadas
        group_by_columns = [getattr(self.table_instance.c, column) for column in columns]
        self.query = self.query.group_by(*group_by_columns)

        return self

    def count(self) -> int:
        """Cuenta el número de registros que cumplen con la consulta actual."""
        if self.query is None:
            raise ValueError("La consulta no está inicializada. Usa el método 'table' primero.")

        # Realizar la consulta de contar los registros sobre la query existente
        count_query = select(func.count()).select_from(self.query.alias())

        with self.db_manager.using_connection() as session:
            result = session.execute(count_query).scalar()  # `.scalar()` para obtener el resultado único

        return result