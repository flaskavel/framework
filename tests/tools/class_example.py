from enum import Enum

class BaseTestClass:
    """
    This is a sample base class for testing reflection.
    It includes methods, properties, and a constant.
    """

    CONSTANT = "This is a constant"

    def __init__(self, value: int):
        self.value = value

    @property
    def squared(self):
        return self.value ** 2

    def method(self):
        return "This is a method"

    @classmethod
    def class_method(cls):
        return "This is a class method"

class TestClass(BaseTestClass):
    """
    This is a sample class for testing reflection.
    It includes methods, properties, and a constant.
    """

    CONSTANT = "This is a constant"

    def __init__(self, value: int):
        self.value = value

    @property
    def squared(self):
        return self.value ** 2

    def method(self):
        return "This is a method"

    @classmethod
    def class_method(cls):
        return "This is a class method"

class TestEnum(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3