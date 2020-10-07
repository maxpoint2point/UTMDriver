from generic.positions import Position
from generic.DocRequest import Request


class NATTNPosition(Position):

    def __init__(self, connector, PositionType, **kwargs):
        super().__init__(PositionType, **kwargs)
        self.connector = connector

    def __str__(self):
        return str(self.WbRegID)

    def resend(self):
        return Request(self.connector, "TTN", TTN=self.WbRegID)