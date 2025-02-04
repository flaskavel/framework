class BaseController:
    """
    BaseController

    This class provides dynamic handling for undefined method calls.
    It mimics the functionality of PHP's `__call` magic method, allowing flexible access to methods.
    """

    def __getattr__(self, method_name):
        """
        Handles access to undefined methods dynamically.

        This method is triggered when attempting to access a method that is not explicitly defined
        in the controller. It dynamically creates a method handler to manage such calls.

        Args:
            method_name (str): The name of the method being accessed.

        Returns:
            function: A dynamically created function that raises an exception when invoked.

        Raises:
            NotImplementedError: If the dynamically created method is invoked, an exception is raised
                                 indicating that the method is not implemented.
        """
        def dynamic_method(*args, **kwargs):
            raise NotImplementedError(
                f"""The method '{method_name}' is not defined in the controller. Please implement this method or ensure the correct method name is being called."""
            )

        return dynamic_method
