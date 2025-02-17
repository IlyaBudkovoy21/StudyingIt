class Valid_token:
    regex = r'[A-Za-z0-9._%+-]+'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value
