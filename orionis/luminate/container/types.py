from orionis.luminate.contracts.container.i_types import ITypes

class Types(ITypes):
    """
    A class that handles validation of primitive types to prevent registering services with primitive-type names.

    This class provides a method to check if a given name corresponds to a primitive type.
    It is used to ensure that services or aliases are not registered with names that conflict
    with Python's built-in primitive types.

    Attributes
    ----------
    _primitive_types : set
        A set containing Python's built-in primitive types and their string representations.

    Methods
    -------
    isPrimitive(name: str) -> bool
        Checks if the provided name corresponds to a primitive type.
    """

    _primitive_types = {
        int, float, str, bool, bytes, type(None), complex,
        list, tuple, dict, set, frozenset,
        "int", "float", "str", "bool", "bytes", "None", "complex",
        "list", "tuple", "dict", "set", "frozenset"
    }

    def isPrimitive(self, name: str) -> bool:
        """
        Checks if the provided name corresponds to a primitive type.

        This method is used to prevent registering services or aliases with names that
        conflict with Python's built-in primitive types.

        Parameters
        ----------
        name : str
            The name of the service or alias to check.

        Returns
        -------
        bool
            True if the name corresponds to a primitive type, False otherwise.

        Raises
        ------
        OrionisContainerException
            If the name matches a primitive type (not implemented in this method).
        """
        return name in self._primitive_types