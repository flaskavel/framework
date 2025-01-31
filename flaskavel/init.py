import argparse
from flaskavel.luminate.installer.init import Init

def main():
    """
    Main entry point for the Flaskavel CLI tool.
    """

    # Create the argument parser for CLI commands
    parser = argparse.ArgumentParser(description="Flaskavel Command Line Tool")

    # Optional argument for displaying the current Flaskavel version
    parser.add_argument('--version', action='store_true', help="Show Flaskavel version.")

    # Optional argument for upgrading Flaskavel to the latest version
    parser.add_argument('--upgrade', action='store_true', help="Upgrade Flaskavel to the latest version.")

    # Command to create a new Flaskavel app (requires an app name)
    parser.add_argument('command', nargs='?', choices=['new'], help="Available command: 'new'.")

    # Name of the application to be created (defaults to 'example-app')
    parser.add_argument('name', nargs='?', help="The name of the Flaskavel application to create.", default="example-app")

    # Parse the provided arguments
    args = parser.parse_args()

    # Initialize the Flaskavel tools for handling operations
    init = Init()

    # Handle the version command
    if args.version:
        init.displayVersion()

    # Handle the upgrade command
    elif args.upgrade:
        init.executeUpgrade()

    # Handle the 'new' command to create a new app
    elif args.command == 'new':
        init.createNewApp(name_app=args.name or 'example-app')

    # If no valid command is provided, show the help message
    else:
        init.displayInfo()

# Execute the main function if the script is run directly
if __name__ == "__main__":
    main()
