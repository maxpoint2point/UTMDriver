from generic.documents.rests.rest import Rest
from generic.helpers.positions import Position
import datetime
from generic.queries.utm import requests


class StoreRest(Rest):
    def __init__(self, connector, xml_data, doc_url):
        self.Position = []
        self.RestDate = datetime.datetime.strptime(
            xml_data.nsDocument.nsReplyRests.rstRestsDate.text,
            "%Y-%m-%dT%H:%M:%S.%f"
        )
        if hasattr(xml_data.nsDocument.nsReplyRests.rstProducts, 'rstStockPosition'):
            for good in xml_data.nsDocument.nsReplyRests.rstProducts.rstStockPosition:
                self.Position.append(
                    Position(
                        'StoreRest',
                        StockPositionQuantity=good.rstQuantity.text,
                        StockPositionInformARegId=good.rstInformARegId.text,
                        StockPositionInformBRegId=good.rstInformBRegId.text,
                        ProductFullName=good.rstProduct.prefFullName.text,
                        ProductAlcCode=good.rstProduct.prefAlcCode.text,
                        ProductCapacity=float(getattr(good.rstProduct, 'prefCapacity', 0)),
                        ProductAlcVolume=float(good.rstProduct.prefAlcVolume),
                        ProductVCode=good.rstProduct.prefProductVCode.text,
                        ProducerClientRegId=good.rstProduct.prefProducer.orefClientRegId.text,
                        ProducerINN=good.rstProduct.prefProducer.orefINN.text,
                        ProducerKPP=good.rstProduct.prefProducer.orefKPP.text,
                        ProducerFullName=good.rstProduct.prefProducer.orefFullName.text,
                        ProducerShortName=good.rstProduct.prefProducer.orefShortName.text,
                        addressCountry=good.rstProduct.prefProducer.orefaddress.orefCountry.text,
                        addressRegionCode=good.rstProduct.prefProducer.orefaddress.orefRegionCode.text,
                        addressDescription=good.rstProduct.prefProducer.orefaddress.orefdescription.text,
                    )
                )
        self.connector = connector
        self.doc_url = doc_url

    def sendToShop(self):
        pass

    def delete(self):
        requests.delete(self.doc_url)
        return True

    def push(self):
        pass

    def __str__(self):
        return f"<{self.RestDate}, [{self.doc_url}]>"
