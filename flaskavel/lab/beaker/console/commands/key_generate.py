from flaskavel.lab.beaker.console.reactor import reactor
from flaskavel.lab.beaker.console.command import Command
from flaskavel.lab.atomic.environment import Env
from cryptography.fernet import Fernet

@reactor.register
class KeyGenerate(Command):
    """
    This command is responsible for initiating the execution of the loops.
    """

    # The command signature used to execute this command.
    signature = 'key:generate'

    # A brief description of the command.
    description = 'Start the execution of the loops loaded in the command Kernel.'

    def handle(self) -> None:

        key = Fernet.generate_key()
        Env.set('APP_KEY', key.decode())

        self.info(
            message="New App Key Generated",
            timestamp=True
        )