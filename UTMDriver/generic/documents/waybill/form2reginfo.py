#  Copyright (c) maxpoint2point@gmail.com 2020.
import datetime
from UTMDriver.generic.helpers.positions import Position


class Form2RegInfo:
    def __init__(self, connector, xml_data, doc_url):
        self.connector = connector
        self.doc_url = doc_url

        self.Identity = xml_data.nsDocument.nsTTNInformF2Reg.wbrHeader.wbrIdentity.text
        self.WBRegId = xml_data.nsDocument.nsTTNInformF2Reg.wbrHeader.wbrWBRegId.text
        self.EGAISFixNumber = xml_data.nsDocument.nsTTNInformF2Reg.wbrHeader.wbrEGAISFixNumber.text
        self.EGAISFixDate = datetime.datetime.strptime(xml_data.nsDocument.nsTTNInformF2Reg.wbrHeader.wbrEGAISFixDate.text, "%Y-%m-%d")
        self.WBNumber = xml_data.nsDocument.nsTTNInformF2Reg.wbrHeader.wbrWBNUMBER.text
        self.WBDate = datetime.datetime.strptime(xml_data.nsDocument.nsTTNInformF2Reg.wbrHeader.wbrWBDate.text, "%Y-%m-%d")
        self.Positions = []

        for position in xml_data.nsDocument.nsTTNInformF2Reg.wbrContent.wbrPosition:
            self.Positions.append(
                Form2Position(
                    PositionType='Form2RegInfo',
                    Identity=int(position.wbrIdentity.text),
                    InformF2Reg=position.wbrInformF2RegId.text,
                    BottlingDate=datetime.datetime.strptime(position.wbrBottlingDate.text, "%Y-%m-%d")
                )
            )


class Form2Position(Position):
    def __init__(self, PositionType, **kwargs):
        super().__init__(PositionType, **kwargs)
