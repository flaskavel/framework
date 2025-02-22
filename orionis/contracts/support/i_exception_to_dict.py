from abc import ABC, abstractmethod

class IExceptionsToDict(ABC):

    @abstractmethod
    def parse(exception):
        """
        Parse the provided exception and serialize it into a dictionary format.

        Parameters
        ----------
        exception : Exception
            The exception object to be serialized.

        Returns
        -------
        dict
            A dictionary containing the exception details such as error type, message,
            and the stack trace.

        Notes
        -----
        - Uses `traceback.TracebackException.from_exception()` to extract detailed traceback information.
        - The stack trace includes filenames, line numbers, function names, and the exact line of code.
        """
        pass