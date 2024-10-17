from enum import Enum

class ConsoleColor(Enum):
    DEFAULT = '\033[0m'          # Default Color
    ERROR_COLOR = '\033[91m'     # Red for errors
    FAIL_COLOR = '\033[31m'      # Another red tone for failures
    INFO_COLOR = '\033[34m'      # Blue for informational messages
    SUCCESS_COLOR = '\033[92m'   # Green for success messages
    UNDERLINE = '\033[4m'        # Underline
    INFO_COLOR_BG = '\033[44m'   # Blue background for INFO
    ERROR_COLOR_BG = '\033[41m'  # Red background for ERROR
    WHITE = '\033[97m'           # White text
    MUTED = '\033[90m'           # Gray (muted) text
    YELLOW_BOLD = '\033[1;33m'   # Yellow bold
    GREEN_BOLD = '\033[1;32m'    # Green bold
    RED_BOLD = '\033[1;31m'      # Red bold