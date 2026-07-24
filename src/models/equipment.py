

class Equipment:
    def __init__(self, name, category, dateBorrowed, laboratory, status, borrower):
        self._name = name
        self._category = category
        self._dateBorrowed = dateBorrowed
        self._laboratory = laboratory
        self._status = status
        self._borrower = borrower

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    @property
    def dateBorrowed(self):
        return self._dateBorrowed

    @dateBorrowed.setter
    def dateBorrowed(self, value):
        self._dateBorrowed = value

    @property
    def laboratory(self):
        return self._laboratory

    @laboratory.setter
    def laboratory(self, value):
        self._laboratory = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def borrower(self):
        return self._borrower

    @borrower.setter
    def borrower(self, value):
        self._borrower = value