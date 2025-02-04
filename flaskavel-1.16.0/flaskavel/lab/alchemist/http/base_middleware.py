class BaseMiddleware:
    """
    BaseMiddleware

    This abstract class serves as the foundation for middleware in the framework.
    It enforces a standard structure for custom middleware by requiring the implementation
    of the `handle` method in all subclasses.
    """

    def handle(self, *args, **kwargs):
        """
        Abstract method to define middleware logic.

        This method must be overridden in subclasses to implement specific middleware behavior.
        It acts as the entry point for middleware logic within the framework.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass. This ensures
                                 that all middleware classes adhere to the expected structure.
        """
        raise NotImplementedError("The 'handle' method must be implemented in the child class.")
