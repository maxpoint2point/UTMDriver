#  Copyright (c) maxpoint2point@gmail.com 2020.

from ....generic.helpers.positions import Position
from ....generic.queries.documents.DocRequest import Request
import random


class NATTNPosition(Position):

    def __init__(self, connector, PositionType, **kwargs):
        super().__init__(PositionType, **kwargs)
        self.connector = connector

    def __str__(self):
        return str(self.WbRegID)

    def resend(self):
        return Request(self.connector, "QueryResendDoc", TTN=self.WbRegID)

    def accept(self):
        return Request(self.connector, "WayBillAct_v3", ttn_id=self.WbRegID, number=random.randint(1, 50))
