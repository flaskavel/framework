import threading

class SingletonMeta(type):
    """
    A thread-safe metaclass for implementing the Singleton pattern.

    This metaclass ensures that only one instance of a class is created,
    even in a multithreaded environment, by using a lock to synchronize
    instance creation.

    Attributes
    ----------
    _instances : dict
        A dictionary that holds the single instances of the classes using this metaclass.
    _lock : threading.Lock
        A lock to ensure thread-safe instance creation.
    """
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        """
        Return the singleton instance of the class in a thread-safe manner.

        If an instance does not already exist, it is created under the protection
        of a lock; otherwise, the existing instance is returned.

        Parameters
        ----------
        *args : list
            Positional arguments for the class constructor.
        **kwargs : dict
            Keyword arguments for the class constructor.

        Returns
        -------
        object
            The singleton instance of the class.
        """
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]