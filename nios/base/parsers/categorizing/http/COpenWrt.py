# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup

from . import CBaseHttpCategorizer


REGEX_LIST = [
    re.compile(r"(?P<url>cgi-bin\/luci)", re.I)
]

REGEX_LIST_VERSIONS = [
    re.compile(r"(?P<name>LEDE) (?:Reboot) (?P<version>[\d.]+)", re.I),
    re.compile(r"(?P<name>OpenWrt) (Chaos Calmer|Attitude Adjustment) (?P<version>[\d.]+(?:[-]rc\d)?)", re.I)
]

class COpenWrt(CBaseHttpCategorizer):

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
        return bool(COpenWrt.getContentMatch(content))

    @staticmethod
    def isHeadersMatch(headers):
        return True

    def execute(self, content, headers):
        result = COpenWrt.getContentMatch(content)

        if 'url' in result:
            url = result.get("url")
            r = self.executeRequest(f"http://{self.mTcpData.ip}:{self.mTcpData.port}/{url}")

            dom = BeautifulSoup(r.content, 'lxml')
            if not dom:
                return

            footer = dom.find("footer")
            hostinfo = dom.find("div", {"class": "hostinfo"})

            info = (footer or hostinfo)

            if not info:
                return

            result = None
            for regex in REGEX_LIST_VERSIONS:
                result = regex.search(info.text)
                if result:
                    break

            if not result:
                return

            d = result.groupdict()
            self.mCategories.add(str(d["name"]).lower())
            self.mCategories.add(str(d["version"]).lower())
            self.mCategories.remove('[RQ_ANALYZE]')

    def executeRequest(self, url):
        try:
            return requests.get(url, timeout=2)
        except Exception:
            return None


    @property
    def categories(self) -> set:
        return self.mCategories
