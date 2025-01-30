import argparse
from flaskavel.luminate.installer.output import Output
from flaskavel.luminate.installer.setup import Setup

def main():
    """
    Main entry point for the Flaskavel CLI.

    Supports:
    - `flaskavel new <app_name>` to create a new Flaskavel app.
    - `flaskavel --version` to display the current version.
    """

    parser = argparse.ArgumentParser(description="Flaskavel Command Line Tool")
    parser.add_argument('--version', action='store_true', help="Show Flaskavel version.")
    parser.add_argument('command', nargs='?', choices=['new'], help="Available command: 'new'.")
    parser.add_argument('name', nargs='?', help="The name of the Flaskavel application to create.", default="example-app")

    try:
        # Parse the arguments
        args = parser.parse_args()

        # Handle --version first (it overrides everything else)
        if args.version:
            Output.asciiArt()
            return

        # Ensure a valid command is provided
        if not args.command:
            Output.error("No command provided. Use 'flaskavel new <app_name>' or 'flaskavel --version'.")
            return

        # Handle 'new' command
        if args.command == 'new':
            if not args.name:
                Output.error("You must specify an application name. Example: 'flaskavel new example-app'")
            else:
                Output.startInstallation()
                Setup(name_app=args.name).handle()
                Output.endInstallation()
            return

    except Exception as e:
        Output.error(f"Fatal Error: {e}")

if __name__ == "__main__":
    main()
