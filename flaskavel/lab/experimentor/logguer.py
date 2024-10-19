import os
import logging
import threading

class Logger:

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Logger, cls).__new__(cls)
                cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):

        path_log_dir = os.path.abspath(os.path.join(__file__, '../../../../../../../storage/logs'))
        os.makedirs(path_log_dir, exist_ok=True)  # Crea la carpeta si no existe

        path_log = os.path.join(path_log_dir, 'flaskavel.log')

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            encoding='utf-8',
            handlers=[
                logging.FileHandler(path_log),
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
        instance = Logger()
        instance.info(message=message)

    @staticmethod
    def error(message: str):
        instance = Logger()
        instance.error(message=message)

    @staticmethod
    def success(message: str):
        instance = Logger()
        instance.success(message=message)

    @staticmethod
    def warning(message: str):
        instance = Logger()
        instance.warning(message=message)
