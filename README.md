# UTMDriver
## Описание
Данный модуль предназначен для интеграции пользовательских приложений с ФСРАР УТМ

Этот модуль представляет собой набор классов и вспомогательных функций для прямой работы с УТМ
## Установка
Клонируем репозиторий в окружение
```
$ git clone https://github.com/maxpoint2point/UTMDriver.git
```
Далее необходимо установить зависимости
## Использование
Импортируем модуль
```
from UTMDriver import Connector
```
Создаем экземпляр УТМ
```
utm = Connector('localhost', 8080)
```
где первый аргумент хост (допускается использование ip), второй порт
* Получение всех документов из базы УТМ
```
utm.getAll()
```
* Получение документов по типу
```
utm.getByType('Ticket')
```
* Получение документов по адресу
```
utm.getByUrl('http://localhost:8080/opt/out/Ticket/5')
```
допускается использование относительного адреса
```
utm.getByUrl('Ticket/5')
```
* Получение документов по ReplyId
```
utm.getByReplyId('7002e49c-5f63-4fdc-8bc7-5a6f8dcda041')
```
Вернет все документы, связанные этим ReplyId

## Отправка исходящих документов
Данный модуль поддерживает отправку некоторых стандартных типов документов в ЕГАИС

Отправка осуществляется с помощью метода класса.
Например, акт списания из торгового зала
```
utm.request_document('ActWriteOfShop_v2', positions=positions, number=4, reason='Иные цели')
```
где переменная позиции может быть списком словарей, содержащие обязательные ключи:
```
positions = {
            'full_name': pos.ProductFullName,
            'alc_code': pos.ProductAlcCode,
            'capacity': pos.ProductCapacity,
            'unit_type': pos.ProductUnitType,
            'alc_volume': pos.ProductAlcVolume,
            'v_code': pos.ProductVCode,
            'Producer_regId': pos.ProducerClientRegId,
            'Producer_inn': pos.ProducerINN,
            'Producer_kpp': pos.ProducerKPP,
            'Producer_fullName': pos.ProducerFullName,
            'Producer_shortName': pos.ProducerShortName,
            'country': pos.addressCountry,
            'region': pos.addressRegionCode,
            'address': pos.addressdescription,
            'quantity': pos.ShopPositionQuantity,
        }
```
Полное описание API Будет в документации