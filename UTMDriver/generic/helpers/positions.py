#  Copyright (c) maxpoint2point@gmail.com 2020.

class Position:
    def __init__(self, PositionType, **kwargs):
        self.type = PositionType
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return f"{self.ProductFullName} ({self.type})"
