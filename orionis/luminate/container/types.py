from orionis.luminate.contracts.container.types_interface import ITypes

class Types(ITypes):
    """A class that handles validation of primitive types to prevent registering services with primitive-type names."""

    # A set of common primitive types in Python
    _primitive_types = {
        int, float, str, bool, bytes, type(None), complex,
        list, tuple, dict, set, frozenset,
        "int", "float", "str", "bool", "bytes", "None", "complex",
        "list", "tuple", "dict", "set", "frozenset"
    }

    def isPrimitive(self, name: str) -> None:
        """Checks if the provided name corresponds to a primitive type.

        Args:
            name (str): The name of the service or alias to check.

        Raises:
            OrionisContainerException: If the name matches a primitive type.
        """
        if name in self._primitive_types:
            return True
        return False