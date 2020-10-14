#  Copyright (c) maxpoint2point@gmail.com 2020.

from UTMDriver.generic.helpers.positions import Position
from UTMDriver.generic.queries.documents.DocRequest import Request


class NATTNPosition(Position):

    def __init__(self, connector, PositionType, **kwargs):
        super().__init__(PositionType, **kwargs)
        self.connector = connector

    def __str__(self):
        return str(self.WbRegID)

    def resend(self):
        return Request(self.connector, "QueryResendDoc", TTN=self.WbRegID)
