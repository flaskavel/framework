import sys
from bootstrap.app import app
from flaskavel.lab.beaker.console.reactor import reactor
from flaskavel.lab.beaker.console.command import Command

@reactor.register
class Serve(Command):

    # The command signature used to execute this command.
    signature = 'serve'

    # A brief description of the command.
    description = 'Starts the development server'

    def handle(self) -> None:
        # Handle the request to start the server and exit with its status.
        status = app().handleRequest()
        sys.exit(status)
