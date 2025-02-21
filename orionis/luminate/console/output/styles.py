from enum import Enum

class ANSIColors(Enum):
    """
    ANSI escape codes for text and background styling in the terminal.

    This Enum provides color codes for text styling in console applications,
    including foreground (TEXT), background (BG), bold (TEXT_BOLD), and
    additional text styles like underlining.

    Attributes
    ----------
    DEFAULT : str
        Resets all colors and styles to default terminal settings.

    Background Colors
    -----------------
    BG_INFO : str
        Blue background, typically used for informational messages.
    BG_ERROR : str
        Red background, typically used for error messages.
    BG_WARNING : str
        Yellow background, typically used for warnings.
    BG_SUCCESS : str
        Green background, typically used for success messages.

    Foreground Colors
    -----------------
    TEXT_INFO : str
        Blue text, typically used for informational messages.
    TEXT_ERROR : str
        Bright red text, typically used for errors.
    TEXT_WARNING : str
        Yellow text, typically used for warnings.
    TEXT_SUCCESS : str
        Green text, typically used for success messages.
    TEXT_WHITE : str
        White text, useful for contrast.
    TEXT_MUTED : str
        Gray text, typically used for secondary/muted information.

    Bold Foreground Colors
    ----------------------
    TEXT_BOLD_INFO : str
        Bold blue text for informational emphasis.
    TEXT_BOLD_ERROR : str
        Bold red text for error emphasis.
    TEXT_BOLD_WARNING : str
        Bold yellow text for warning emphasis.
    TEXT_BOLD_SUCCESS : str
        Bold green text for success emphasis.
    TEXT_BOLD_WHITE : str
        Bold white text for strong contrast.
    TEXT_BOLD_MUTED : str
        Bold gray text for muted yet emphasized information.

    Additional Text Styles
    ----------------------
    TEXT_BOLD : str
        Bold text style.
    TEXT_STYLE_UNDERLINE : str
        Underlined text for emphasis.
    TEXT_RESET : str
        Resets text styles to default settings.
    """

    DEFAULT = '\033[0m'                 # Reset all colors and styles

    # Background Colors
    BG_INFO = '\033[44m'                # Blue background for INFO
    BG_ERROR = '\033[41m'               # Red background for ERROR
    BG_FAIL = '\033[48;5;166m'          # Red background for FAIL
    BG_WARNING = '\033[43m'             # Yellow background for WARNING
    BG_SUCCESS = '\033[42m'             # Green background for SUCCESS

    # Foreground Text Colors
    TEXT_INFO = '\033[34m'              # Blue for informational messages
    TEXT_ERROR = '\033[91m'             # Bright red for errors
    TEXT_WARNING = '\033[33m'           # Yellow for warnings
    TEXT_SUCCESS = '\033[32m'           # Green for success
    TEXT_WHITE = '\033[97m'             # White text
    TEXT_MUTED = '\033[90m'             # Gray (muted) text

    # Bold Foreground Text Colors
    TEXT_BOLD_INFO = '\033[1;34m'       # Bold blue for INFO
    TEXT_BOLD_ERROR = '\033[1;91m'      # Bold red for ERROR
    TEXT_BOLD_WARNING = '\033[1;33m'    # Bold yellow for WARNING
    TEXT_BOLD_SUCCESS = '\033[1;32m'    # Bold green for SUCCESS
    TEXT_BOLD_WHITE = '\033[1;97m'      # Bold white text
    TEXT_BOLD_MUTED = '\033[1;90m'      # Bold gray (muted) text

    # Additional Text Styles
    TEXT_BOLD = "\033[1m"               # Bold text
    TEXT_STYLE_UNDERLINE = '\033[4m'    # Underline text
    TEXT_RESET = "\033[0m"              # Reset styles
    CYAN = "\033[36m"
    DIM = "\033[2m"
    MAGENTA = "\033[35m"
    ITALIC = "\033[3m"