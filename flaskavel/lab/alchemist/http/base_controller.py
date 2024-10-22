class BaseController:

    def __getattr__(self, method_name):
        """
        This method is called when trying to access a method that does not exist.
        It allows for dynamic handling of method calls, similar to PHP's __call.

        Args:
            method_name (str): The name of the method being accessed.

        Returns:
            function: A dynamically created method function.
        """
        def dynamic_method(*args, **kwargs):
            raise NotImplementedError(
                f"The method '{method_name}' is not defined in the controller. "
                "Please implement this method or ensure the correct method name is being called."
            )

        return dynamic_method
