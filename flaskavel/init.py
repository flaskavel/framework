import argparse
from flaskavel.luminate.installer.output import Output
from flaskavel.luminate.installer.setup import Setup
from flaskavel.luminate.installer.upgrade import Upgrade

def main():
    """
    Main entry point for the Flaskavel CLI.

    Supports:
    - `flaskavel new <app_name>` to create a new Flaskavel app.
    - `flaskavel --version` to display the current version.
    - `flaskavel --upgrade` to upgrade Flaskavel to the latest version.
    """

    parser = argparse.ArgumentParser(description="Flaskavel Command Line Tool")
    parser.add_argument('--version', action='store_true', help="Show Flaskavel version.")
    parser.add_argument('--upgrade', action='store_true', help="Upgrade Flaskavel to the latest version.")
    parser.add_argument('command', nargs='?', choices=['new'], help="Available command: 'new'.")
    parser.add_argument('name', nargs='?', help="The name of the Flaskavel application to create.", default="example-app")

    try:
        # Parse the arguments
        args = parser.parse_args()

        # Handle --version first (it overrides everything else)
        if args.version:
            Output.asciiArt()

        # Handle --upgrade command
        if args.upgrade:
            try:
                Output.info("Starting the upgrade process...")
                Upgrade.execute()
                Output.info("Flaskavel has been successfully upgraded!")
                Output.asciiArt()
            except Exception as e:
                Output.error(f"Fatal Error: {e}")

        # Ensure a valid command is provided
        if not args.command:
            Output.error("No command provided. Use 'flaskavel new <app_name>', 'flaskavel --version', or 'flaskavel --upgrade'.")

        # Handle 'new' command
        if args.command == 'new':
            if not args.name:
                Output.error("You must specify an application name. Example: 'flaskavel new example-app'")

            Output.startInstallation()
            Setup(name_app=args.name).handle()
            Output.endInstallation()


    except Exception as e:
        Output.error(f"Fatal Error: {e}")

if __name__ == "__main__":
    main()
