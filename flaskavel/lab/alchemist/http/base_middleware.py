class BaseMiddleware:

    def __init__(self):
        pass

    def handle(self, *args, **kwargs):
        raise NotImplementedError("The 'handle' method must be implemented in the child class.")
