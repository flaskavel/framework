class DotDict(dict):

    """
    A dictionary subclass that allows access to dictionary values using dot notation, with handling for missing keys.
    This class extends the built-in `dict` class to provide attribute-style access to dictionary keys. If a key is not found,
    it returns `None` instead of raising a `KeyError`. Additionally, nested dictionaries are automatically converted to `DotDict`
    instances.
    Methods
    -------
    __getattr__(item)
        Retrieves the value associated with the given key using dot notation. If the key does not exist, returns `None`.
        If the value is a dictionary, it is converted to a `DotDict` instance.
    """

    def __getattr__(self, item):
        """
        Retrieves the value associated with the given key using dot notation. If the key does not exist, returns `None`.
        If the value is a dictionary, it is converted to a `DotDict` instance.
        """

        # Retrieve the value associated with the key
        value = self.get(item, None)

        # If the value is a dictionary, convert it to a DotDict instance
        if isinstance(value, dict):
            return DotDict(value)

        # Otherwise, return the value
        return value