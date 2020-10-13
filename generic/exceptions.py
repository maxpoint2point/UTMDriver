#  Copyright (c) maxpoint2point@gmail.com 2020.

class UTMNotConnect(Exception):
    """Нет соединения к УТМ"""
    pass


class EmptyResponse(Exception):
    """В ответе нет необходимых данных"""
    pass


class DocumentNotFound(Exception):
    """Документ не найден в УТМ"""
    pass


class UnsupportedDocument(Exception):
    pass


class MissingArgument(Exception):
    pass


class TypeMismatch(Exception):
    pass
