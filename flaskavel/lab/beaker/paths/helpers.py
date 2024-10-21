import os
from flaskavel.lab.catalyst.paths import _Paths

def app_path(file:str=None):
    path_dir = _Paths().get_directory('app')
    if file:
        return os.path.abspath(os.path.join(path_dir, file))
    return path_dir

def bootstrap_path(file:str=None):
    path_dir = _Paths().get_directory('bootstrap')
    if file:
        return os.path.abspath(os.path.join(path_dir, file))
    return path_dir

def config_path(file:str=None):
    path_dir = _Paths().get_directory('config')
    if file:
        return os.path.abspath(os.path.join(path_dir, file))
    return path_dir

def database_path(file:str=None):
    path_dir = _Paths().get_directory('database')
    if file:
        return os.path.abspath(os.path.join(path_dir, file))
    return path_dir

def public_path(file:str=None):
    path_dir = _Paths().get_directory('public')
    if file:
        return os.path.abspath(os.path.join(path_dir, file))
    return path_dir

def resource_path(file:str=None):
    path_dir = _Paths().get_directory('resource')
    if file:
        return os.path.abspath(os.path.join(path_dir, file))
    return path_dir

def routes_path(file:str=None):
    path_dir = _Paths().get_directory('routes')
    if file:
        return os.path.abspath(os.path.join(path_dir, file))
    return path_dir

def storage_path(file:str=None):
    path_dir = _Paths().get_directory('storage')
    if file:
        return os.path.abspath(os.path.join(path_dir, file))
    return path_dir

def tests_path(file:str=None):
    path_dir = _Paths().get_directory('tests')
    if file:
        return os.path.abspath(os.path.join(path_dir, file))
    return path_dir