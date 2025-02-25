import traceback
from orionis.luminate.contracts.support.i_exception_to_dict import IExceptionsToDict

class ExceptionsToDict(IExceptionsToDict):
    """
    A utility class to parse an exception and convert it into a structured dictionary.

    Methods
    -------
    parse(exception: Exception) -> dict
        Converts an exception into a dictionary containing the error type, message,
        and stack trace information.
    """

    @staticmethod
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
        # Extract the detailed traceback information from the exception
        tb = traceback.TracebackException.from_exception(exception)

        # Construct and return the dictionary containing all necessary exception details
        return {
            "error_type": tb.exc_type_str,  # Using `exc_type_str` to avoid deprecation warnings
            "error_message": str(tb),  # A string representation of the entire traceback message
            "stack_trace": [
                {
                    "filename": frame.filename,  # The source file of the frame
                    "lineno": frame.lineno,      # The line number where the exception occurred
                    "name": frame.name,          # The function name
                    "line": frame.line           # The line of code in the frame
                }
                for frame in tb.stack  # Iterating over each frame in the traceback stack
            ]
        }
