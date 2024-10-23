from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from flaskavel.lab.beaker.console.reactor import reactor
from flaskavel.lab.beaker.console.command import Command
from flaskavel.lab.atomic.environment import Env

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
        # Set the desired cipher for key generation
        cipher = 'AES-256-G9M'

        # Determine the key length based on the specified cipher
        if '128' in cipher and 'AES' in cipher and 'GCM' in cipher:
            length = 128
        elif '192' in cipher and 'AES' in cipher and 'GCM' in cipher:
            length = 192
        elif '256' in cipher and 'AES' in cipher and 'GCM' in cipher:
            length = 256
        else:
            # Log an error message if no valid cipher is configured
            self.line("No valid cipher configured in 'config/app.py://cipher'. Defaulting to 'AES-256-GCM'.")
            length = 256  # Default length

        # Generate a new AES-GCM key of the specified length and convert it to a hexadecimal string
        new_key = AESGCM.generate_key(bit_length=length).hex()

        # Store the generated key in the environment under 'APP_KEY'
        Env.set('APP_KEY', new_key)

        # Limit the message to 68 characters, showing the first 4 and last 4 characters of the key
        masked_key = f"{new_key[:4]}{'•' * (len(new_key) - 8)}{new_key[-4:]}"

        # Prepare the final message ensuring it stays within the 68 character limit
        message = f"New AES-{length}-GCM App Key Generated: APP_KEY = {masked_key}"

        # Log the message with a timestamp
        self.info(message=message[:68], timestamp=True)

