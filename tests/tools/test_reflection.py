import os
import unittest
from orionis.luminate.tools.reflection import Reflection
from tests.tools.class_example import BaseTestClass, TestClass, TestEnum

class TestReflection(unittest.TestCase):

    def setUp(self):
        """Set up the test case."""
        self.reflection = Reflection(TestClass)

    def test_get_file(self):
        """Test if the file path is correctly retrieved."""
        path = self.reflection.getFile().split(os.sep)
        self.assertEqual(path[-1], "class_example.py")

    def test_has_class(self):
        """Test if the class is loaded."""
        self.assertTrue(self.reflection.hasClass())

    def test_has_method(self):
        """Test if the class has specific methods."""
        self.assertTrue(self.reflection.hasMethod("method"))
        self.assertFalse(self.reflection.hasMethod("non_existent_method"))

    def test_has_property(self):
        """Test if the class has specific properties."""
        self.assertTrue(self.reflection.hasProperty("squared"))
        self.assertFalse(self.reflection.hasProperty("non_existent_property"))

    def test_has_constant(self):
        """Test if the class has specific constants."""
        self.assertTrue(self.reflection.hasConstant("CONSTANT"))
        self.assertFalse(self.reflection.hasConstant("NON_EXISTENT_CONSTANT"))

    def test_get_attributes(self):
        """Test if the class attributes (methods, properties) are retrieved."""
        attributes = self.reflection.getAttributes()
        self.assertIn("method", attributes)
        self.assertIn("squared", attributes)

    def test_get_constructor(self):
        """Test if the constructor is correctly retrieved."""
        constructor = self.reflection.getConstructor()
        self.assertEqual(constructor.__name__, "__init__")

    def test_get_docstring(self):
        """Test if the docstring is correctly retrieved."""
        doc = self.reflection.getDocComment()
        self.assertIn("sample class for testing reflection", doc)

    def test_get_file_name(self):
        """Test if the file name where the class is defined is retrieved."""
        file_name = self.reflection.getFileName(remove_extension=True)
        self.assertEqual(file_name, "class_example")

    def test_get_method(self):
        """Test if a specific method is correctly retrieved."""
        method = self.reflection.getMethod("method")
        self.assertIsNotNone(method)

    def test_get_methods(self):
        """Test if all methods are correctly retrieved."""
        methods = self.reflection.getMethods()
        self.assertGreater(len(methods), 0)

    def test_get_name(self):
        """Test if the class name is correctly retrieved."""
        name = self.reflection.getName()
        self.assertEqual(name, "TestClass")

    def test_get_parent_class(self):
        """Test if the parent classes are correctly retrieved."""
        parent = self.reflection.getParentClass()
        self.assertTrue(self.reflection.isSubclassOf(BaseTestClass))

    def test_get_properties(self):
        """Test if the class properties are correctly retrieved."""
        properties = self.reflection.getProperties()
        self.assertIn("squared", properties)

    def test_get_property(self):
        """Test if a specific property is correctly retrieved."""
        property_value = self.reflection.getProperty("squared")
        self.assertIsNotNone(property_value)

    def test_is_abstract(self):
        """Test if the class is abstract."""
        self.assertFalse(self.reflection.isAbstract())

    def test_is_enum(self):
        """Test if the class is an enum."""
        enum_reflection = Reflection(TestEnum)
        self.assertTrue(enum_reflection.isEnum())

    def test_is_subclass_of(self):
        """Test if the class is a subclass of the specified parent."""
        self.assertTrue(self.reflection.isSubclassOf(BaseTestClass))

    def test_is_instance_of(self):
        """Test if the class is an instance of the specified class."""
        instance = TestClass(5)
        self.assertTrue(self.reflection.isInstanceOf(instance))

    def test_is_iterable(self):
        """Test if the class is iterable."""
        self.assertFalse(self.reflection.isIterable())

    def test_is_instantiable(self):
        """Test if the class is instantiable."""
        self.assertTrue(self.reflection.isInstantiable())

    def test_new_instance(self):
        """Test if a new instance of the class can be created."""
        instance = self.reflection.newInstance(5)
        self.assertEqual(instance.value, 5)

    def test_class_method_and_property(self):
        """Test if class methods and properties work for an instance."""
        instance = self.reflection.newInstance(5)
        self.assertEqual(instance.class_method(), "This is a class method")
        self.assertEqual(instance.squared, 25)

    def test_str_representation(self):
        """Test the string representation of the reflection instance."""
        str_rep = str(self.reflection)
        self.assertIn("Orionis Reflection class", str_rep)
        self.assertIn("TestClass", str_rep)
