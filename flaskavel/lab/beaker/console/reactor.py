import time
from flaskavel.lab.experimentor.logguer import Log
from flaskavel.lab.beaker.console.output import Console

class Reactor:
    """
    A class for registering and executing commands within the framework.
    """

    def __init__(self):
        """
        Initializes the Reactor instance.
        """
        self.commands = {}
        self.start_time = time.time()

    def register(self, command_class):
        """
        Registers a command class, extracting its signature and description.

        Args:
            command_class (type): The command class to register, which must have
                                  `signature` and `description` attributes.

        Returns:
            type: The registered command class.
        """
        # Extract the command signature and description
        signature = command_class.signature
        description = command_class.description

        # Register the command using its signature
        self.commands[signature] = {
            'class': command_class,
            'signature': str(signature).strip(),
            'description': str(description).strip(),
        }

        return command_class

    def call(self, signature, args):
        """
        Executes a registered command by its signature.

        Args:
            signature (str): The signature of the command to execute.
            *args: Additional positional arguments to pass to the command's handle method.
            **kwargs: Additional keyword arguments to pass to the command's handle method.

        Prints:
            A message indicating if the command was not found.
        """

        exceptions = ['loops:run', 'schedule:work']
        print_console = signature not in exceptions

        command_entry = self.commands.get(signature)

        if not command_entry:
            raise ValueError("The command not exist.")

        try:

            if print_console:
                Console.executeTimestamp(command=signature, state='RUNNING')

            command_class = command_entry['class']
            command_instance = command_class()
            command_instance._setArguments()
            command_instance._argumentsParse(args)
            command_instance.handle()

            execution_duration = int((time.time() - self.start_time) * 1000)

            if print_console:
                Console.executeTimestamp(command=signature, seconds=f"{execution_duration}ms", state='DONE')

            Log.info(f"Command '{signature}' executed successfully.")

        except Exception as e:

            message = f"Command '{signature}' execution failed. Error: {e}"

            if print_console:
                Console.executeTimestamp(command=signature, state='FAIL')
                Console.error(message)

            Log.error(message)

# Create a global instance of the Reactor
reactor = Reactor()
