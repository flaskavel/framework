from abc import ABC, abstractmethod

class InstallerSetup(ABC):
    """
    Interface for the InstallerSetup class.
    """

    @abstractmethod
    def _sanitize_folder_name(self, name: str) -> str:
        """
        Sanitize the provided folder name to ensure it is valid across different operating systems.

        Steps:
        1. Normalize text to remove accents and special characters.
        2. Convert to lowercase.
        3. Replace spaces with underscores.
        4. Remove invalid characters.
        5. Strip leading and trailing whitespace.
        6. Enforce length limit (255 characters).
        7. Ensure the result contains only valid characters.

        Parameters
        ----------
        name : str
            The original folder name to sanitize.

        Returns
        -------
        str
            The sanitized folder name.

        Raises
        ------
        ValueError
            If the sanitized folder name is empty or contains invalid characters.
        """
        pass

    @abstractmethod
    def handle(self):
        """
        Executes the setup process for initializing the Orionis project.

        This process includes:
        1. Cloning the repository.
        2. Creating a virtual environment.
        3. Installing dependencies from requirements.txt.
        4. Setting up the .env file.
        5. Generating an API key.
        6. Cleaning up temporary files and .git remote origin.

        Raises
        ------
        ValueError
            If there is an error during any subprocess execution.
        Exception
            If any unexpected error occurs.
        """
        pass