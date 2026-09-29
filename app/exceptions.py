class TheError(Exception):
    def __init__(self, message="Error e was occured!"):
        super().__init__(message)