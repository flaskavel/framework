class OrionisContainerException(Exception):
    """
    Excepción personalizada para errores relacionados con el contenedor de inyección de dependencias Orionis.
    """

    def __init__(self, message: str) -> None:
        """
        Inicializa la excepción con un mensaje de error.

        Args:
            message (str): Mensaje descriptivo del error.
        """
        super().__init__(message)

    def __str__(self) -> str:
        """Retorna una representación en cadena de la excepción."""
        return f"[OrionisContainerException] {self.args[0]}"


class OrionisContainerValueError(ValueError):
    """
    Excepción personalizada para errores de tipo ValueError en el contenedor Orionis.
    """

    def __init__(self, message: str) -> None:
        """
        Inicializa la excepción con un mensaje de error.

        Args:
            message (str): Mensaje descriptivo del error.
        """
        super().__init__(message)

    def __str__(self) -> str:
        """Retorna una representación en cadena de la excepción."""
        return f"[OrionisContainerValueError] {self.args[0]}"

class OrionisContainerTypeError(TypeError):
    """
    Custom exception for TypeError related to the Orionis container.
    """

    def __init__(self, message: str) -> None:
        """
        Initializes the exception with an error message.

        Args:
            message (str): Descriptive error message.
        """
        super().__init__(message)

    def __str__(self) -> str:
        """Returns a string representation of the exception."""
        return f"[OrionisContainerTypeError] {self.args[0]}"
