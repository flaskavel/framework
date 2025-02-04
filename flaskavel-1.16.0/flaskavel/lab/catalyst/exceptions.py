class DumpFlaskavelException(Exception):
    """
    Custom exception raised when there is an issue with dumping the Flaskavel data.

    Args:
        response (str): The response message associated with the exception.
    """
    def __init__(self, response):
        self.response = response

class AuthorizeFlaskavelException(Exception):
    """
    Custom exception raised when there is an authorization failure in Flaskavel.

    Args:
        response (str): The response message associated with the exception.
    """
    def __init__(self, response):
        self.response = response

class ValidateFlaskavelException(Exception):
    """
    Custom exception raised when there is a validation failure in Flaskavel.

    Args:
        response (str): The response message associated with the exception.
    """
    def __init__(self, response):
        self.response = response
