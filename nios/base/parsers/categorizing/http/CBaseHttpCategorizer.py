# -*- coding: utf-8 -*-

class CBaseHttpCategorizer:

    def __init__(self, categories, tcpData):
        pass

    @staticmethod
    def isContentMatch(content):
        raise NotImplementedError

    @staticmethod
    def isHeadersMatch(headers):
        raise NotImplementedError

    def execute(self, content, headers):
        raise NotImplementedError

    @property
    def categories(self) -> set:
        raise NotImplementedError