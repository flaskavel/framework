import argparse
from flaskavel.metadata import NAME, VERSION
from flaskavel.luminate.installer.output import Output
from flaskavel.luminate.installer.setup import Setup

def main():
    """
    Main entry point for the Flaskavel CLI.

    Supports:
    - `flaskavel new <app_name>` to create a new Flaskavel app.
    - `flaskavel --version` to display the current version.
    """

    # Startup message
    Output.welcome()

    # Create the argument parser
    parser = argparse.ArgumentParser(description="Flaskavel Command Line Tool")

    # Add '--version' option
    parser.add_argument('--version', action='store_true', help="Show Flaskavel version.")

    # Define the main command ('new') and its argument
    parser.add_argument('command', nargs='?', choices=['new'], help="Available command: 'new'.")
    parser.add_argument('name', nargs='?', help="The name of the Flaskavel application to create.")

    try:
        # Parse the arguments
        args = parser.parse_args()

        # Handle --version first (it overrides everything else)
        if args.version:
            print(f"Flaskavel v{VERSION}")
            return

        # Ensure a valid command is provided
        if not args.command:
            Output.error("No command provided. Use 'flaskavel new <app_name>' or 'flaskavel --version'.")

        # Handle 'new' command
        if args.command == 'new':
            if not args.name:
                Output.error("You must specify an application name. Example: 'flaskavel new example-app'")
            else:
                Setup(name_app=args.name).handle()
                Output.finished()

    except SystemExit:
        Output.error("Invalid arguments. Use 'flaskavel new <app_name>' or 'flaskavel --version'.")
    except Exception as e:
        Output.error(f"Fatal Error: {e}")

if __name__ == "__main__":
    main()
