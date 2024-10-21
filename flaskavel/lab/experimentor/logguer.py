import os
import logging
import threading

class Logguer:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, path: str = None):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Logguer, cls).__new__(cls)
                cls._instance._initialize_logger(path)
        return cls._instance

    def _initialize_logger(self, path: str = None):

        if not path:
            path_log_dir = os.path.abspath(os.path.join(__file__, '../../../../../../../storage/logs'))
            os.makedirs(path_log_dir, exist_ok=True)
            path_log = os.path.join(path_log_dir, 'flaskavel.log')
            path = path_log

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            encoding='utf-8',
            handlers=[
                logging.FileHandler(path),
            ]
        )
        self.logger = logging.getLogger()

    def info(self, message: str):
        self.logger.info(message)

    def error(self, message: str):
        self.logger.error(message)

    def success(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def debug(self, message: str):
        self.logger.debug(message)

class Log:

    @staticmethod
    def info(message: str):
        instance = Logguer()
        instance.info(message=message)

    @staticmethod
    def error(message: str):
        instance = Logguer()
        instance.error(message=message)

    @staticmethod
    def success(message: str):
        instance = Logguer()
        instance.success(message=message)

    @staticmethod
    def warning(message: str):
        instance = Logguer()
        instance.warning(message=message)
