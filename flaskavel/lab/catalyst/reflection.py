from enum import Enum
import importlib
import inspect

class Reflection:
    def __init__(self, classname: str = None, module: str = None):
        self.classname = classname
        self.module_name = module
        self.cls = None
        if module:
            self.safe_import()

    def safe_import(self):
        """Safely import a class from a module."""
        try:
            module = importlib.import_module(self.module_name)
            if self.classname:
                self.cls = getattr(module, self.classname, None)
                if self.cls is None:
                    raise ValueError(f"Class '{self.classname}' not found in module '{self.module_name}'.")
        except ImportError as e:
            raise ValueError(f"Error importing module '{self.module_name}': {e}")

    def has_class(self) -> bool:
        """Check if the class exists in the module."""
        return self.cls is not None

    def has_method(self, method_name: str) -> bool:
        """Check if the class has the specified method."""
        return hasattr(self.cls, method_name)

    def has_property(self, prop: str) -> bool:
        """Check if the class has the specified property."""
        return hasattr(self.cls, prop)

    def has_constant(self, constant: str) -> bool:
        """Check if the class/module has a constant."""
        return hasattr(self.cls, constant)

    def get_attributes(self) -> list:
        """Get all attributes of the class."""
        return dir(self.cls) if self.cls else []

    def get_constructor(self):
        """Get the class constructor (__init__)."""
        return self.cls.__init__ if self.cls else None

    def get_doc_comment(self) -> str:
        """Get the docstring of the class."""
        return self.cls.__doc__ if self.cls else None

    def get_file_name(self) -> str:
        """Get the file name where the class is defined."""
        return inspect.getfile(self.cls) if self.cls else None

    def get_method(self, method_name: str):
        """Get a specific method of the class."""
        return getattr(self.cls, method_name, None) if self.cls else None

    def get_methods(self) -> list:
        """Get all methods of the class."""
        return inspect.getmembers(self.cls, predicate=inspect.isfunction) if self.cls else []

    def get_name(self) -> str:
        """Get the full name of the class."""
        return self.cls.__name__ if self.cls else None

    def get_parent_class(self):
        """Get the parent class if available."""
        return self.cls.__bases__ if self.cls else None

    def get_properties(self) -> list:
        """Get all properties of the class."""
        return [prop for prop in dir(self.cls) if isinstance(getattr(self.cls, prop), property)] if self.cls else []

    def get_property(self, prop: str):
        """Get the value of a property."""
        return getattr(self.cls, prop, None) if self.cls else None

    def is_abstract(self) -> bool:
        """Check if the class is abstract."""
        return hasattr(self.cls, '__abstractmethods__') and bool(self.cls.__abstractmethods__) if self.cls else False

    def is_enum(self) -> bool:
        """Check if the class is an enum."""
        return isinstance(self.cls, type) and issubclass(self.cls, Enum) if self.cls else False

    def is_iterable(self) -> bool:
        """Check if the class is iterable."""
        return hasattr(self.cls, '__iter__') if self.cls else False

    def is_instantiable(self) -> bool:
        """Check if the class can be instantiated."""
        return self.cls is not None and callable(self.cls) and not self.is_abstract()

    def new_instance(self, *args, **kwargs):
        """Create a new instance of the class."""
        if self.is_instantiable():
            return self.cls(*args, **kwargs)
        raise TypeError(f"Cannot instantiate class '{self.classname}'.")

    def __str__(self) -> str:
        """String representation of the class."""
        return f"<Reflection class '{self.classname}' in module '{self.module_name}'>"
