class UserCodeWrongError(Exception):
    pass


class APIError(Exception):
    pass


class UnexpectedError(Exception):
    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)
