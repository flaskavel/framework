from flaskavel.luminate.contracts.tools.std_interface import IStdClass

class StdClass(IStdClass):
    """
    A dynamic class that allows setting arbitrary attributes,
    similar to PHP's stdClass.
    """

    def __init__(self, **kwargs):
        """
        Initializes the StdClass with optional keyword arguments.

        Parameters
        ----------
        kwargs : dict
            Key-value pairs to set as attributes.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        """
        Returns a string representation of the object.

        Returns
        -------
        str
            A formatted string showing the object's attributes.
        """
        return f"{self.__class__.__name__}({self.__dict__})"

    def toDict(self):
        """
        Converts the object's attributes to a dictionary.

        Returns
        -------
        dict
            A dictionary representation of the object's attributes.
        """
        return self.__dict__

    def update(self, **kwargs):
        """
        Updates the object's attributes dynamically.

        Parameters
        ----------
        kwargs : dict
            Key-value pairs to update attributes.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
