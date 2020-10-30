#  Copyright (c) maxpoint2point@gmail.com 2020.

from ....generic.documents.waybill import waybill
import datetime
from ....generic.helpers.positions import Position


class WayBill_v3(waybill.WayBill):
    def __init__(self, connector, xml_data, doc_url):
        self.Position = []
        self.connector = connector
        self.doc_url = doc_url
        self.Identity = xml_data.nsDocument.nsWayBill_v3.wbIdentity.text
        self.TTNId = None  # TODO: Доделать
        self.NUMBER = xml_data.nsDocument.nsWayBill_v3.wbHeader.wbNUMBER.text
        self.Date = datetime.datetime.strptime(
            xml_data.nsDocument.nsWayBill_v3.wbHeader.wbDate.text,
            "%Y-%m-%d"
        )
        self.ShippingDate = datetime.datetime.strptime(
            xml_data.nsDocument.nsWayBill_v3.wbHeader.wbShippingDate.text,
            "%Y-%m-%d"
        )
        self.Type = xml_data.nsDocument.nsWayBill_v3.wbHeader.wbType.text
        self.ShipperClientRegId = xml_data.nsDocument.nsWayBill_v3.wbHeader.wbShipper.orefUL.orefClientRegId.text
        self.ShipperFullName = xml_data.nsDocument.nsWayBill_v3.wbHeader.wbShipper.orefUL.orefFullName.text
        self.ShipperShortName = xml_data.nsDocument.nsWayBill_v3.wbHeader.wbShipper.orefUL.orefShortName.text
        self.ShipperINN = xml_data.nsDocument.nsWayBill_v3.wbHeader.wbShipper.orefUL.orefINN.text
        self.ShipperKPP = xml_data.nsDocument.nsWayBill_v3.wbHeader.wbShipper.orefUL.orefKPP.text
        self.ShipperCountry = xml_data.nsDocument.nsWayBill_v3.wbHeader.wbShipper.orefUL.orefaddress.orefCountry.text
        self.ShipperRegionCode = xml_data.nsDocument.nsWayBill_v3.wbHeader.wbShipper.orefUL.orefaddress.orefRegionCode.text
        self.ShipperDescription = xml_data.nsDocument.nsWayBill_v3.wbHeader.wbShipper.orefUL.orefaddress.orefdescription.text
        self.ConsigneeClientRegId = xml_data.nsDocument.nsWayBill_v3.wbHeader.wbConsignee.orefFL.orefClientRegId.text
        self.ConsigneeFullName = xml_data.nsDocument.nsWayBill_v3.wbHeader.wbConsignee.orefFL.orefFullName.text
        self.ConsigneeShortName = xml_data.nsDocument.nsWayBill_v3.wbHeader.wbConsignee.orefFL.orefShortName.text
        self.ConsigneeINN = xml_data.nsDocument.nsWayBill_v3.wbHeader.wbConsignee.orefFL.orefINN.text
        self.ConsigneeKPP = str(getattr(xml_data.nsDocument.nsWayBill_v3.wbHeader.wbConsignee.orefFL, "orefKPP", ''))
        self.ConsigneeCountry = xml_data.nsDocument.nsWayBill_v3.wbHeader.wbConsignee.orefFL.orefaddress.orefCountry.text
        self.ConsigneeRegionCode = xml_data.nsDocument.nsWayBill_v3.wbHeader.wbConsignee.orefFL.orefaddress.orefRegionCode.text
        self.ConsigneeDescription = xml_data.nsDocument.nsWayBill_v3.wbHeader.wbConsignee.orefFL.orefaddress.orefdescription.text
        self.TRAN_TYPE = str(getattr(xml_data.nsDocument.nsWayBill_v3.wbHeader.wbTransport, 'wbTRAN_TYPE', ''))
        self.TRAN_COMPANY = str(getattr(xml_data.nsDocument.nsWayBill_v3.wbHeader.wbTransport, 'wbTRAN_COMPANY', ''))
        self.TRAN_CAR = xml_data.nsDocument.nsWayBill_v3.wbHeader.wbTransport.wbTRAN_CAR.text
        self.TRAN_DRIVER = xml_data.nsDocument.nsWayBill_v3.wbHeader.wbTransport.wbTRAN_DRIVER.text
        self.TRAN_LOADPOINT = xml_data.nsDocument.nsWayBill_v3.wbHeader.wbTransport.wbTRAN_LOADPOINT.text
        self.TRAN_UNLOADPOINT = xml_data.nsDocument.nsWayBill_v3.wbHeader.wbTransport.wbTRAN_UNLOADPOINT.text
        self.TRAN_FORWARDER = str(getattr(xml_data.nsDocument.nsWayBill_v3.wbHeader.wbTransport, 'wbTRAN_FORWARDER', ''))
        self.Base = str(getattr(xml_data.nsDocument.nsWayBill_v3.wbHeader, 'wbBase', ''))
        self.Note = str(getattr(xml_data.nsDocument.nsWayBill_v3.wbHeader, 'wbNote', ''))

        for goods in xml_data.nsDocument.nsWayBill_v3.wbContent.wbPosition:
            self.Position.append(
                Position(
                    "WayBill_v3",
                    Identity=int(goods.wbIdentity.text),
                    Type=goods.wbProduct.prefType.text,
                    FullName=goods.wbProduct.prefFullName.text,
                    AlcCode=goods.wbProduct.prefAlcCode.text,
                    Capacity=float(getattr(goods.wbProduct, 'prefCapacity', 0)),
                    UnitType=goods.wbProduct.prefUnitType.text,
                    AlcVolume=float(goods.wbProduct.prefAlcVolume.text),
                    ProductVCode=goods.wbProduct.prefProductVCode.text,
                    ProducerClientRegId=goods.wbProduct.prefProducer.orefUL.orefClientRegId.text,
                    ProducerFullName=goods.wbProduct.prefProducer.orefUL.orefFullName.text,
                    ProducerShortName=goods.wbProduct.prefProducer.orefUL.orefShortName.text,
                    ProducerINN=goods.wbProduct.prefProducer.orefUL.orefINN.text,
                    ProducerKPP=goods.wbProduct.prefProducer.orefUL.orefKPP.text,
                    ProducerCountry=goods.wbProduct.prefProducer.orefUL.orefaddress.orefCountry.text,
                    ProducerRegionCode=goods.wbProduct.prefProducer.orefUL.orefaddress.orefRegionCode.text,
                    ProducerAddressDescription=goods.wbProduct.prefProducer.orefUL.orefaddress.orefdescription.text,
                    Quantity=float(goods.wbQuantity.text),
                    Price=float(goods.wbPrice.text),
                    FARegId=goods.wbFARegId.text,
                    F2RegId=goods.wbInformF2.ceF2RegId.text,
                )
            )

    def accept(self):
        pass

    def reject(self):
        pass

    def delete(self):
        pass

    def __str__(self):
        pass
