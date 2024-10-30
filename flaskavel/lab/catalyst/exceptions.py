class DumpFlaskavelException(Exception):
    def __init__(self, response):
        self.response = response

class AuthorizeFlaskavelException(Exception):
    def __init__(self, response):
        self.response = response

class ValidateFlaskavelException(Exception):
    def __init__(self, response):
        self.response = response