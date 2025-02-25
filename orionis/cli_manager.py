import argparse
from orionis.installer.manager import InstallerManager
from orionis.installer.output.output import InstallerOutput

# Main entry point for the Orionis CLI tool.
def main():

    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Orionis Command Line Tool")
    parser.add_argument('--version', action='store_true', help="Show Orionis version.")
    parser.add_argument('--upgrade', action='store_true', help="Upgrade Orionis to the latest version.")
    parser.add_argument('command', nargs='?', choices=['new'], help="Available command: 'new'.")
    parser.add_argument('name', nargs='?', help="The name of the Orionis application to create.", default="example-app")

    # Parse the provided arguments
    args = parser.parse_args()

    # Initialize the Orionis tools for handling operations
    try:
        installer = InstallerManager()
        if args.version:
            installer.handleVersion()
        elif args.upgrade:
            installer.handleUpgrade()
        elif args.command == 'new':
            installer.handleNewApp(args.name)
        else:
            installer.handleInfo()
    except Exception as e:
        InstallerOutput.error(f"An error occurred: {e}", e)

# Execute the main function if the script is run directly
if __name__ == "__main__":
    main()
