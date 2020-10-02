from documents.rests.rest import *
from generic.positions import Position
import datetime


class StoreRest(Rest):
    def __init__(self, connector, xml_data, doc_url):
        self.RestDate = datetime.datetime.strptime(
            xml_data.nsDocument.nsReplyRests.rstRestsDate.text,
            "%Y-%m-%dT%H:%M:%S.%f"
        )
        for good in xml_data.nsDocument.nsReplyRests.rstProducts.rstStockPosition:
            self.Position.append(
                Position(
                    'StoreRest',
                    StockPositionQuantity=good.rstQuantity.text,
                    StockPositionInformARegId=good.rstInformARegId.text,
                    StockPositionInformBRegId=good.rstInformBRegId.text,
                    ProductFullName=good.rstProduct.prefFullName.text,
                    ProductAlcCode=good.rstProduct.prefAlcCode.text,
                    ProductCapacity=good.rstProduct.prefCapacity.text,
                    ProductAlcVolume=good.rstProduct.prefAlcVolume.text,
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

    def delete(self):
        pass

    def push(self):
        pass

    def __str__(self):
        return f"{self.RestDate}, {self.doc_url}"
