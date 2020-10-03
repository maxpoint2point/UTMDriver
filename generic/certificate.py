import datetime


class Certificate:
    def __init__(self, **kwargs):
        self.CN = kwargs.get('cn')
        self.SURNAME = kwargs.get('surname')
        self.GIVENNAME = kwargs.get('givenname')
        self.C = kwargs.get('c')
        self.ST = kwargs.get('st')
        self.L = kwargs.get('l')
        self.STREET = kwargs.get('street')
        self.EMAILADDRESS = kwargs.get('emailaddress')
        self.ValidityFrom = datetime.datetime.strptime(kwargs['valid_from'], "%a %b %d %H:%M:%S MSK %Y")
        self.ValidityTo = datetime.datetime.strptime(kwargs['valid_to'], "%a %b %d %H:%M:%S MSK %Y")
        self.certType = kwargs['cert']

    def __bool__(self):
        if self.ValidityTo > datetime.datetime.today():
            return True
        else:
            return False

    @property
    def isValid(self):
        return self.__bool__()

    @property
    def daysToEnd(self):
        return self.ValidityTo - datetime.datetime.today()
