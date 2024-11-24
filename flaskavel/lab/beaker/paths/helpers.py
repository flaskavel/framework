import os
from flaskavel.lab.catalyst.paths import _Paths

def app_path(file: str = None):
    """
    Retrieves the absolute path to the 'app' directory, optionally appending a file.

    Args:
        file (str, optional): Filename to append to the 'app' directory path.

    Returns:
        str: Absolute path to the 'app' directory or specified file within it.
    """
    # Get the base directory for 'app'
    path_dir = _Paths().get_directory('app')

    if file:  # Append file to path if provided
        return os.path.abspath(os.path.join(path_dir, file))

    # Return the base path if no file specified
    return path_dir

def bootstrap_path(file: str = None):
    """
    Retrieves the absolute path to the 'bootstrap' directory, optionally appending a file.

    Args:
        file (str, optional): Filename to append to the 'bootstrap' directory path.

    Returns:
        str: Absolute path to the 'bootstrap' directory or specified file within it.
    """
    path_dir = _Paths().get_directory('bootstrap')

    if file:
        return os.path.abspath(os.path.join(path_dir, file))

    return path_dir

def config_path(file: str = None):
    """
    Retrieves the absolute path to the 'config' directory, optionally appending a file.

    Args:
        file (str, optional): Filename to append to the 'config' directory path.

    Returns:
        str: Absolute path to the 'config' directory or specified file within it.
    """
    path_dir = _Paths().get_directory('config')

    if file:
        return os.path.abspath(os.path.join(path_dir, file))

    return path_dir

def database_path(file: str = None):
    """
    Retrieves the absolute path to the 'database' directory, optionally appending a file.

    Args:
        file (str, optional): Filename to append to the 'database' directory path.

    Returns:
        str: Absolute path to the 'database' directory or specified file within it.
    """
    path_dir = _Paths().get_directory('database')

    if file:
        return os.path.abspath(os.path.join(path_dir, file))

    return path_dir

def public_path(file: str = None):
    """
    Retrieves the absolute path to the 'public' directory, optionally appending a file.

    Args:
        file (str, optional): Filename to append to the 'public' directory path.

    Returns:
        str: Absolute path to the 'public' directory or specified file within it.
    """
    path_dir = _Paths().get_directory('public')

    if file:
        return os.path.abspath(os.path.join(path_dir, file))

    return path_dir

def resource_path(file: str = None):
    """
    Retrieves the absolute path to the 'resource' directory, optionally appending a file.

    Args:
        file (str, optional): Filename to append to the 'resource' directory path.

    Returns:
        str: Absolute path to the 'resource' directory or specified file within it.
    """
    path_dir = _Paths().get_directory('resource')

    if file:
        return os.path.abspath(os.path.join(path_dir, file))

    return path_dir

def routes_path(file: str = None):
    """
    Retrieves the absolute path to the 'routes' directory, optionally appending a file.

    Args:
        file (str, optional): Filename to append to the 'routes' directory path.

    Returns:
        str: Absolute path to the 'routes' directory or specified file within it.
    """
    path_dir = _Paths().get_directory('routes')

    if file:
        return os.path.abspath(os.path.join(path_dir, file))

    return path_dir

def storage_path(file: str = None):
    """
    Retrieves the absolute path to the 'storage' directory, optionally appending a file.

    Args:
        file (str, optional): Filename to append to the 'storage' directory path.

    Returns:
        str: Absolute path to the 'storage' directory or specified file within it.
    """
    path_dir = _Paths().get_directory('storage')

    if file:
        return os.path.abspath(os.path.join(path_dir, file))

    return path_dir

def tests_path(file: str = None):
    """
    Retrieves the absolute path to the 'tests' directory, optionally appending a file.

    Args:
        file (str, optional): Filename to append to the 'tests' directory path.

    Returns:
        str: Absolute path to the 'tests' directory or specified file within it.
    """
    path_dir = _Paths().get_directory('tests')

    if file:
        return os.path.abspath(os.path.join(path_dir, file))

    return path_dir