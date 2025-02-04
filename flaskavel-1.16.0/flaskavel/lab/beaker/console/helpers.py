import datetime

def strftime(format: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    Returns the current date and time as a formatted string.

    Args:
        format (str): The format in which to return the date and time.
                      Default is '%Y-%m-%d %H:%M:%S'.

    Returns:
        str: The current date and time formatted as specified.
    """

    # Get the current date and time
    current_datetime = datetime.datetime.now()

    # Format the current date and time based on the specified format
    return current_datetime.strftime(format)
