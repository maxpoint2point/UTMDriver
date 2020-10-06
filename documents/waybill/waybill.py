from abc import ABC, abstractmethod


class WayBill(ABC):
    Identity = None
    TTNId = None
    NUMBER = None  # РН00013530
    Date = None
    ShippingDate = None
    Type = None  # WBInvoiceFromMe
    ShipperClientRegId = None
    ShipperFullName = None
    ShipperShortName = None
    ShipperINN = None
    ShipperKPP = None
    ShipperCountry = None
    ShipperRegionCode = None
    ShipperDescription = None  # Россия, 353682, КРАСНОДАРСКИЙ край, МИЧУРИНА ул, ЕЙСК г, ДОМ 4
    ConsigneeClientRegId = None  # 030000414982
    ConsigneeFullName = None
    ConsigneeShortName = None
    ConsigneeINN = None
    ConsigneeKPP = None
    ConsigneeCountry = None
    ConsigneeRegionCode = None
    ConsigneeDescription = None  # г.Ейск, п.Широчанка, ул.Восточная, д. 44
    TRAN_TYPE = None  # Тип транспорта
    TRAN_COMPANY = None  # ООО ТЗБ
    TRAN_CAR = None  # Газель
    TRAN_DRIVER = None  # Экспедитор
    TRAN_LOADPOINT = None  # Точка загрузки
    TRAN_UNLOADPOINT = None  # Точка разгрузки
    TRAN_FORWARDER = None  # Экспедитор
    Base = None
    Note = None
    Position = []

    @abstractmethod
    def accept(self):
        pass

    @abstractmethod
    def reject(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def __str__(self):
        pass
