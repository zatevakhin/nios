# -*- coding: utf-8 -*-

import re
import logging
import requests
from bs4 import BeautifulSoup

from . import CBaseHttpCategorizer


REGEX_LIST = [
    re.compile(r'redirect_suffix[\s]=[\s]"/(?P<url>redirect\.html)\?(?P<arg_count>count)="\+Math\.random\(\);', re.I),
]

class CQnap(CBaseHttpCategorizer):

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
        return bool(CQnap.getContentMatch(content))

    @staticmethod
    def isHeadersMatch(headers):
        return headers.get("server") in ["http server 1.0"]

    def execute(self, content, headers):
        result = CQnap.getContentMatch(content)

        if "url" in result and "arg_count" in result:
            self.executeQnapRegex1(content, headers)

    def executeQnapRegex1(self, content, headers):

        def getTagValue(dom, tagName):
            tag = dom.find(tagName)
            if tag:
                return tag.text

        url = f"http://{self.mTcpData.ip}:{self.mTcpData.port}/cgi-bin/authLogin.cgi"

        responce = self.executeRequest(url)
        if responce is None:
            logging.warning("if responce is None")
            return

        content = responce.content.decode()
        dom = BeautifulSoup(content, features="xml")

        tagValues = [
            getTagValue(dom, "version"),
            getTagValue(dom, "build"),
            getTagValue(dom, "platform"),
            getTagValue(dom, "modelName")
        ]

        tagValues = list(filter(bool, tagValues))

        if not tagValues:
            logging.warning("if not tagValues")
            return

        tagValues = list(map(lambda x: str(x).lower(), tagValues))

        tagValues.append("qnap")
        tagValues.append("nas")

        self.mCategories.remove('[RQ_ANALYZE]')
        self.mCategories = set(self.mCategories | set(tagValues))

    def executeRequest(self, url):
        try:
            return requests.get(url, timeout=2)
        except Exception:
            return None

    @property
    def categories(self) -> set:
        return self.mCategories
