# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup

from . import CBaseHttpCategorizer


REGEX_LIST = [
    re.compile(r"(?P<url>Main_Login.asp)", re.I)
]


class CAsus(CBaseHttpCategorizer):

    def __init__(self, categories: set, tcpData):
        self.mCategories: set = categories
        self.mTcpData = tcpData

    @staticmethod
    def getContentMatch(content):
        for regex in REGEX_LIST:
            result = regex.search(content.decode())
            if result:
                return result.groupdict()

    @staticmethod
    def isContentMatch(content):
        return bool(CAsus.getContentMatch(content))

    @staticmethod
    def isHeadersMatch(headers):
        return headers.get("server") in ["httpd/2.0"]

    def execute(self, content, headers):
        result = CAsus.getContentMatch(content)

        if 'url' in result:
            url = result.get("url")
            r = self.executeRequest(f"http://{self.mTcpData.ip}:{self.mTcpData.port}/{url}")

            dom = BeautifulSoup(r.content, 'lxml')

            if not dom:
                return

            title = dom.find("title")
            if not title:
                return

            if title.text not in ["ASUS Login"]:
                return

            madelName = dom.find("div", {"class": "prod_madelName"})
            if not madelName:
                return

            self.mCategories.add(str(madelName.text).lower())
            self.mCategories.remove('[RQ_ANALYZE]')


    def executeRequest(self, url):
        try:
            return requests.get(url, timeout=2)
        except Exception:
            return None


    @property
    def categories(self) -> set:
        return self.mCategories
