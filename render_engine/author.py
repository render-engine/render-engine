class Author:
    def __init__(self, email: str, name: str=''):
        self.email = email
        self.name = name

    def __str__(self):
        if self.name:
            return f'{self.email} ({self.name})'

        else:
            return self.email
