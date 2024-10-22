from flaskavel.lab.reagents.request import Request

class BaseMiddleware:

    def __init__(self, module: str, classname: str, method: str):
        """
        Initializes the middleware with the module, the controller class, and the method to invoke.

        Args:
            module (str): The name of the module where the controller is located.
            classname (str): The name of the controller class.
            method (str): The name of the method to invoke in the controller.
        """
        self.module = module
        self.classname = classname
        self.method = method

    def next(self, *args, **kwargs):
        """
        Dynamically creates an instance of the controller and calls the specified method.

        Args:
            *args: Positional arguments passed to the controller method.
            **kwargs: Keyword arguments passed to the controller method.
        """
        # Import the controller module dynamically using the provided module name
        controller_module = __import__(self.module, fromlist=[self.classname])
        # Get the controller class from the imported module
        controller_class = getattr(controller_module, self.classname)

        # Create an instance of the controller class
        instance_controller = controller_class()

        # Call the specified method with the provided arguments
        return getattr(instance_controller, self.method)(*args, Request())

    def handle(self, *args, **kwargs):
        """
        Method that must be implemented in the child class to handle the request.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.
        """
        raise NotImplementedError("The 'handle' method must be implemented in the child class.")
