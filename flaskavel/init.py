import argparse
from flaskavel.luminate.installer.output import Output
from flaskavel.luminate.installer.setup import Setup

def main():
    """
    Main entry point for the Flaskavel App Creation Tool.

    This function handles the argument parsing, validation, and initiates the app creation process.
    It ensures that the provided arguments are valid, creates a new Flaskavel app, and provides feedback
    throughout the process.

    Steps:
    1. Outputs a welcome message using Output.welcome().
    2. Parses command-line arguments using argparse.
    3. Validates the 'command' and 'name_app' arguments.
    4. Calls Setup to handle the app creation process.
    5. Outputs the completion message using Output.finished().

    Raises
    ------
    SystemExit : If invalid arguments are provided, prints error and exits.
    Exception : For any unexpected errors during the execution process.
    """

    # Startup message
    Output.welcome()

    # Create the argument parser
    parser = argparse.ArgumentParser(description="Flaskavel App Creation Tool")

    # Required 'new' command and app name
    parser.add_argument('command', choices=['new'], help="Command must be 'new'.")
    parser.add_argument('name', help="The name of the Flaskavel application to create.")

    try:
        # Parse the arguments
        args = parser.parse_args()

        # Validate command (this is already done by 'choices')
        if args.command != 'new':
            Output.error("Unrecognized command, did you mean 'flaskavel new example-app'?")

        # Validate app name (empty check is not needed because argparse handles that)
        if not args.name:
            Output.error("You must specify an application name, did you mean 'flaskavel new example-app'?")

        # Create and run the app setup process
        app = Setup(name_app=str(args.name).strip())
        app.handle()

        # Startup finished
        Output.finished()

    except SystemExit as e:
        # Handles invalid arguments and prints usage error
        Output.error("Invalid arguments. Usage example: 'flaskavel new example-app'")
    except Exception as e:
        # Handles any other unexpected errors
        Output.error(f"Fatal Error: {e}")

if __name__ == "__main__":
    main()
