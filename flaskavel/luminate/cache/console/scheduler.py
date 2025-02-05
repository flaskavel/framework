class CacheScheduler():

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.schedulers = {}
        return cls._instance

    def register(self, command_signature: str, params : dict, frequency: str):
        self.schedulers[command_signature] = {
            'command_signature':command_signature,
            'params':params,
            'frequency':frequency
        }

    def unregister(self, signature: str):
        if signature not in self.commands:
            raise KeyError(f"Command '{signature}' not found.")
        del self.commands[signature]

    def get(self, signature: str):
        command = self.commands.get(signature)
        if not command:
            raise KeyError(f"Command with signature '{signature}' not found.")
        return command
