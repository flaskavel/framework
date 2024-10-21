from flaskavel.lab.catalyst.environment import _Environment

def env(key:str, default=None):
    return Env.get(key, default)

class Env:

    @staticmethod
    def get(key: str, default=None):
        """
        Método estático para obtener el valor de una variable de entorno.

        Args:
            key (str): La clave de la variable de entorno.
            default: Valor predeterminado si la clave no existe.

        Returns:
            El valor de la variable de entorno o el valor predeterminado.
        """
        environment = _Environment()  # Obtiene la instancia Singleton
        return environment.get(key=key, default=default)

    @staticmethod
    def set(key: str, value: str):
        """
        Método estático para establecer el valor de una variable de entorno.

        Args:
            key (str): La clave de la variable de entorno.
            value (str): El valor a establecer.

        Returns:
            None
        """
        environment = _Environment()  # Obtiene la instancia Singleton
        environment.set(key=key, value=value)

    @staticmethod
    def unset(key: str):
        """
        Método estático para eliminar una variable de entorno.

        Args:
            key (str): La clave de la variable de entorno a eliminar.

        Returns:
            None
        """
        environment = _Environment()  # Obtiene la instancia Singleton
        environment.unset(key=key)

    @staticmethod
    def get_values():
        """
        Método estático para obtener todos los valores de las variables de entorno.

        Returns:
            dict: Un diccionario con todas las variables de entorno.
        """
        environment = _Environment()  # Obtiene la instancia Singleton
        return environment.get_values()

    @staticmethod
    def get_path():
        """
        Método estático para obtener la ruta del archivo .env.

        Returns:
            str: La ruta del archivo .env.
        """
        environment = _Environment()  # Obtiene la instancia Singleton
        return environment.get_path()
