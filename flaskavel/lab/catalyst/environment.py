import os
import threading
from dotenv import get_key, set_key, unset_key, dotenv_values

class _Environment:

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, path: str = None):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(_Environment, cls).__new__(cls)
                cls._instance._initialize(path)
        return cls._instance

    def _initialize(self, path: str = None):
        self.path = path
        if not self.path:
            self.path = os.path.join(__file__, '../../../../../../../.env')


    def get(self, key: str, default=None):
        """
        Obtiene el valor de una variable de entorno.

        Args:
            key (str): La clave de la variable de entorno.
            default: Valor predeterminado si la clave no existe.

        Returns:
            El valor de la variable de entorno o el valor predeterminado.
        """

        if key not in dotenv_values(dotenv_path=self.path):
            return default

        return get_key(dotenv_path=self.path, key_to_get=key)


    def set(self, key: str, value: str):
        """
        Establece el valor de una variable de entorno.

        Args:
            key (str): La clave de la variable de entorno.
            value (str): El valor a establecer.

        Returns:
            None
        """
        set_key(dotenv_path=self.path, key_to_set=str(key), value_to_set=str(value))

    def unset(self, key: str):
        """
        Elimina una variable de entorno.

        Args:
            key (str): La clave de la variable de entorno a eliminar.

        Returns:
            None
        """
        unset_key(dotenv_path=self.path, key_to_unset=str(key))

    def get_values(self):
        """
        Obtiene todos los valores de las variables de entorno.

        Returns:
            dict: Un diccionario con todas las variables de entorno.
        """
        return dotenv_values(dotenv_path=self.path)

    def get_path(self):
        """
        Obtiene la ruta del archivo .env.

        Returns:
            str: La ruta del archivo .env.
        """
        return self.path