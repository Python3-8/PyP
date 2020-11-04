class Error:
    def __init__(self, msg):
        self.msg = msg

    def raise_(self):
        print(type(self).__name__ + ': ' + self.msg)

    def __bool__(self):
        return False


class InvalidSyntaxError(Error):
    pass
