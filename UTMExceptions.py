class UTMNotConnect(Exception):
    """Нет соединения к УТМ"""
    pass

class EmptyResponse(Exception):
    """В ответе нет необходимых данных"""
    pass

class DocumentNotFound(Exception):
    """Документ не найден в УТМ"""
    pass