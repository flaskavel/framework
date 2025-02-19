from abc import ABC, abstractmethod

class ITypes(ABC):
    """A class that handles validation of primitive types to prevent registering services with primitive-type names."""

    @abstractmethod
    def isPrimitive(self, name: str) -> None:
        """Checks if the provided name corresponds to a primitive type.

        Args:
            name (str): The name of the service or alias to check.

        Raises:
            OrionisContainerException: If the name matches a primitive type.
        """
    pass