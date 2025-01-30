from abc import ABC, abstractmethod

class IUpgrade(ABC):
    """
    Interface for the Upgrade process in Flaskavel.

    This interface enforces the implementation of methods required to handle
    upgrading Flaskavel to the latest version.
    """

    @staticmethod
    @abstractmethod
    def execute() -> None:
        """
        Executes the upgrade process for Flaskavel.

        This method should be implemented to define the upgrade logic, ensuring 
        the application is updated to the latest available version.

        Raises
        ------
        ValueError
            If the upgrade process fails or encounters any error during execution.
        """
        pass
