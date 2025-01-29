from abc import ABC, abstractmethod

class SetupInterface(ABC):
    """
    Abstract base class for setup operations.

    This interface defines a contract for setup classes, requiring the implementation
    of the `handle` method to execute setup logic.

    Methods
    -------
    handle()
        Abstract method that must be implemented by subclasses to define setup behavior.
    """

    @abstractmethod
    def handle(self):
        """
        Execute the setup process.

        This method must be implemented by any subclass to perform the necessary
        setup actions. The specific implementation details depend on the subclass.

        Raises
        ------
        NotImplementedError
            If the method is not implemented in a subclass.
        """
        pass
