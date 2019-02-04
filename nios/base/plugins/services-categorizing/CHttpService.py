#-*- coding: utf-8 -*-

import logging
import re

import requests
from bs4 import BeautifulSoup

from nios.base.parsers.categorizing import CHttpCategorizersManager
from nios.core.auxiliary import exception
from nios.core.CJsonObjectManager import CJsonObjectManager
from nios.core.CNiosCore import CNiosCore
from nios.core.data import CTask, ETaskPriority, ETaskType
from nios.core.data.CTcpConnectResult import CTcpConnectResult
from nios.core.plugins.CPluginBase import CPluginBase


SERVICE_TYPE = "http"
SERVICE_CLASS = "passive"
ACTION_CLASS = "analyze"

IGNORE_CODES = [403, 404, 500]


class CollectByRegexGroups:

    def __init__(self, regexGroups):
        self.mRegexGroups = regexGroups

    def findMatch(self, regex, string: str):
        match = re.match(regex, string, re.I)

        if not match:
            return

        groupdict = match.groupdict()

        if groupdict:
            return groupdict

        return True


    def groupIterator(self, group, string: str):
        regexList = group.get("regex-list")
        regexListName = group.get("name")
        regexListType = group.get("type")

        for regex in regexList:
            match = self.findMatch(regex, string)

            if match is not None:
                data = {
                    "vendor": regexListName,
                    "type": regexListType
                }

                if isinstance(match, dict):
                    data.update({**match})
                return data


    def __call__(self, string: str):

        if not string:
            return

        for group in self.mRegexGroups:
            data = self.groupIterator(group, string)
            if data:
                return data



class CHttpService(CPluginBase):

    mName = f'{SERVICE_TYPE}-service'
    mTags = {SERVICE_TYPE, SERVICE_CLASS, ACTION_CLASS}

    def __init__(self, core: CNiosCore):
        self.mCore = core
        self.mTaggingData = CJsonObjectManager("config/tagging.data.json")

    def __call__(self, task: CTask):
        result = self.executeRequest(task)

        if not isinstance(result, requests.Response):
            logging.warning("Request error!")
            return None

        if result.status_code in IGNORE_CODES:
            logging.warning(f"Status code '{result.status_code}' ignored")
            return None

        headers = {k.lower(): v for k, v in dict(result.headers).items()}

        task.data.update({f"{SERVICE_TYPE}": {
            "code": result.status_code,
            "content": result.content,
            "headers": headers
        }})

        self.tryCollectServiceInfo(task)

        print(self.__call__.__name__, task.data.get("collected"))

        return task

    def tryCollectServiceInfo(self, task: CTask):
        self.collectFromHeaders(task)
        self.collectFromContent(task)

    def collectFromHeaders(self, task: CTask):
        self.analyzeServerType(task)
        self.analyzeWwwAuthenticateType(task)


    def analyzeServerType(self, task: CTask):
        headers = task.data.get(f"{SERVICE_TYPE}", {}).get("headers", {})
        server = headers.get("server", None)

        if not server:
            return

        regexGroups = self.mTaggingData.get("server-groups", [])
        collector = CollectByRegexGroups(regexGroups)

        collected = collector(server)

        if not collected:
            return

        task.data["collected"].update(collected)

    def analyzeWwwAuthenticateType(self, task: CTask):
        headers = task.data.get(f"{SERVICE_TYPE}", {}).get("headers", {})
        wwwAuthenticate = headers.get("www-authenticate", None)

        print("www-authenticate: ", wwwAuthenticate)

        if not wwwAuthenticate:
            return None

        regexGroups = self.mTaggingData.get("regex-groups", [])
        collector = CollectByRegexGroups(regexGroups)

        wwwAuthenticateMatch = {}

        match = re.search(r"(?P<auth>Basic|Digest)", wwwAuthenticate, re.I)
        if match:
            groupdict = (match.groupdict() or {})
            wwwAuthenticateMatch = {**groupdict, **wwwAuthenticateMatch}

        match = re.search(r"realm=[\"\'](?P<realm>.*?)[\"\']", wwwAuthenticate, re.I)
        if match:
            groupdict = (match.groupdict() or {})
            wwwAuthenticateMatch = {**groupdict, **wwwAuthenticateMatch}

        match = re.search(r"qop=[\"\'](?P<qop>\w+)[\"\']", wwwAuthenticate, re.I)
        if match:
            groupdict = (match.groupdict() or {})
            wwwAuthenticateMatch = {**groupdict, **wwwAuthenticateMatch}

        match = re.search(r"nonce=[\"\'](?P<nonce>\w+)[\"\']", wwwAuthenticate, re.I)
        if match:
            groupdict = (match.groupdict() or {})
            wwwAuthenticateMatch = {**groupdict, **wwwAuthenticateMatch}

        match = re.search(r"algorithm=(?P<algorithm>\w+)", wwwAuthenticate, re.I)
        if match:
            groupdict = (match.groupdict() or {})
            wwwAuthenticateMatch = {**groupdict, **wwwAuthenticateMatch}

        if not wwwAuthenticateMatch:
            return

        realm = wwwAuthenticateMatch.pop("realm", None)
        print("realm: ", realm)

        if wwwAuthenticateMatch:
            task.data["collected"].update(wwwAuthenticateMatch)

        collected = collector(realm)

        if not collected:
            return

        task.data["collected"].update(collected)

    def collectFromContent(self, task: CTask):
        content = task.data.get(f"{SERVICE_TYPE}", {}).get("content", None)

        if not content:
            return

        dom = BeautifulSoup(content, 'lxml')
        title = dom.find('title')

        if not title:
            return None

        title = str(title.text).strip()
        print("title: ", title)

        regexGroups = self.mTaggingData.get("regex-groups", []) # todo: title groups
        collector = CollectByRegexGroups(regexGroups)

        collected = collector(title)

        if not collected:
            return

        task.data["collected"].update(collected)


    def executeRequest(self, task: CTask):
        tcpData: CTcpConnectResult = task.data.get("tcp")

        httpTimeout = self.mCore.mConfig.get("timeout.http", 2)

        try:
            url = f"http://{tcpData.ip}:{tcpData.port}"
            logging.debug(url)
            return requests.get(url, timeout=httpTimeout)
        except Exception:
            # logging.exception(exception)
            return None

    def onComplete(self, task: CTask):
        if not task:
            return

        task.type = ETaskType.SERVICES_VULNERABILITY_CHECK
        task.priority = ETaskPriority.HIGH
        self.mCore.put(task)

    def onError(self, error):
        logging.exception(error)

    # def detailedAnalysis(self, categories: set, headers: dict, content: str, tcpData: CTcpConnectResult):

    #     updatedCategories = categories
    #     if REQUIRES_ANALYZE in categories:
    #         httpCategorizers = CHttpCategorizersManager(tcpData)
    #         updatedCategories = httpCategorizers.execute(categories, headers, content)

        # return updatedCategories
