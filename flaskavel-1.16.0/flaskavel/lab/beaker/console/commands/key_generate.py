from flaskavel.lab.catalyst.config import Config
from flaskavel.lab.atomic.environment import Env
from flaskavel.lab.beaker.console.reactor import reactor
from flaskavel.lab.beaker.console.command import Command
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

@reactor.register
class KeyGenerate(Command):
    """
    The KeyGenerate command is responsible for generating a new cryptographic key
    according to the configured cipher specifications and saving it in the environment file.
    """

    # The command signature used to execute this command.
    signature = 'key:generate'

    # A brief description of the command.
    description = 'Generates a new key in the environment file.'

    def handle(self) -> None:
        """
        Executes the command to generate and store a new application key by performing the following steps:
        1. Determines the cipher and key length based on application configuration.
        2. Generates an AES-GCM key of the specified length.
        3. Saves the generated key in the environment file under the key 'APP_KEY'.
        4. Logs a masked version of the key for security purposes.

        Returns:
            None
        """

        try:

            # Set the desired cipher for key generation
            cipher = Config.app('cipher')

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
                # Default length
                length = 256

            # Generate a new AES-GCM key of the specified length and convert it to a hexadecimal string
            new_key = AESGCM.generate_key(bit_length=length).hex()

            # Store the generated key in the environment under 'APP_KEY'
            Env.set('APP_KEY', new_key)

            # Mask the key for logging, showing only the first and last 4 characters
            masked_key = f"{new_key[:4]}{'•' * (len(new_key) - 8)}{new_key[-4:]}"

            # Prepare the final message ensuring it stays within the 68 character limit
            message = f"New AES-{length}-GCM App Key Generated: APP_KEY = {masked_key}"

            # Log the masked key with a timestamp
            self.info(message=message[:68], timestamp=True)

        except Exception as e:

            # Display general error message for any unexpected issue
            self.error(f"An unexpected error occurred: {e}", timestamp=True)
            exit(1)
