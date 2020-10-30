#  Copyright (c) maxpoint2point@gmail.com 2020.
from ....generic.helpers.positions import Position


class TTNHistoryF2Reg:
    def __init__(self, connector, xml_data, doc_url):
        self.Step = []
        self.WbRegId = xml_data.nsDocument.nsTTNHistoryF2Reg.wbrHeader.wbrWBRegId.text
        self.connector = connector
        self.doc_url = doc_url

        for step in xml_data.nsDocument.nsTTNHistoryF2Reg.wbrContent.wbrPosition.wbrHistF2.wbrstep:
            self.Step.append(
                Step(
                    lev=int(step.wbrlev.text),
                    Form2=step.wbrForm2.text,
                    parentForm2=step.wbrparentForm2.text,
                    Shipper=step.wbrShipper.text,
                    Consignee=step.wbrConsignee.text,
                    WbRegId=step.wbrWBRegId.text,
                    amount=step.wbramount.text,
                    PositionType='TTNHistoryF2Reg'
                )
            )


class Step(Position):
    def __init__(self, PositionType, **kwargs):
        super().__init__(PositionType, **kwargs)
