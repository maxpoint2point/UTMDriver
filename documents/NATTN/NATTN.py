import datetime

from documents.NATTN.Position import NATTNPosition
from generic import UtmRequest


class ReplyNATTN:
    def __init__(self, connector, xml_data, doc_url):
        self.Position = []
        self.ReplyDate = datetime.datetime.strptime(
            xml_data.nsDocument.nsReplyNoAnswerTTN.ttnReplyDate.text,
            "%Y-%m-%dT%H:%M:%S.%f"
        )
        self.connector = connector
        self.doc_url = doc_url
        self.Consignee = xml_data.nsDocument.nsReplyNoAnswerTTN.ttnConsignee

        for ttn in xml_data.nsDocument.nsReplyNoAnswerTTN.ttnttnlist.ttnNoAnswer:
            self.Position.append(
                NATTNPosition(
                    self.connector,
                    'ReplyNATTN',
                    WbRegID=ttn.ttnWbRegID,
                    ttnNumber=ttn.ttnttnNumber,
                    ttnDate=datetime.datetime.strptime(ttn.ttnttnDate.text, "%Y-%m-%d"),
                    Shipper=ttn.ttnShipper,
                )
            )

    def delete(self):
        UtmRequest.delete(self.doc_url)
        return True

    def __str__(self):
        return f"<ReplyNATNN [{self.ReplyDate}]>"
