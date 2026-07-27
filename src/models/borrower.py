class Borrower:
    def __init__(self, name, number, email):
        self._id = None
        self._name = name
        self._number = number
        self._email = email

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        self._number = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value