class AWSError(Exception):
    def __init__(self, message: str, exception):
        self.message = f"{message} \nRaised Exception: {exception}"
        super().__init__(self.message)
