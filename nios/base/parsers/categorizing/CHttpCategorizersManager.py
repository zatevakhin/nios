# -*- coding: utf-8 -*-

from .http import CQnap, CAsus, COpenWrt

import re


CATEGORIZERS_LIST = [
    CAsus, COpenWrt, CQnap
]


class CHttpCategorizersManager:

    def __init__(self, tcpData):
        self.mTcpData = tcpData

    def execute(self, categories, headers, content):

        for categorizer in CATEGORIZERS_LIST:
            isContentMatch = categorizer.isContentMatch(content)
            isHeadersMatch = categorizer.isHeadersMatch(headers)
            print(categorizer, isContentMatch, isHeadersMatch)

            if isContentMatch and isHeadersMatch:
                obj = categorizer(categories, self.mTcpData)
                obj.execute(content, headers)

                if "[RQ_ANALYZE]" not in obj.categories:
                    return obj.categories

        return categories

