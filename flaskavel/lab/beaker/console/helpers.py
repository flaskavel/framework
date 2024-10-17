import datetime

def strftime(format : str = '%Y-%m-%d %H:%M:%S'):
    current_datetime = datetime.datetime.now()
    return current_datetime.strftime(format)
