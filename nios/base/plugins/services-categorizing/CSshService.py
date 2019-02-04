# #-*- coding: utf-8 -*-

# import logging
# import re

# from nios.core.plugins.CPluginBase import CPluginBase
# from nios.core.CNiosCore import CNiosCore
# from nios.core.auxiliary import exception
# from nios.core.CScheduler import CTask
# from nios.core.CScheduler import ETaskPriority

# from nios.core.data.CTcpConnectResult import CTcpConnectResult


# regexList = [
#     re.compile(r"SSH-\d\.\d-(?P<server>dropbear)_(?P<version>(?:\d{4})\.(?:\d+))", re.I),
#     re.compile(r"SSH-\d\.\d-(?P<server>OpenSSH)_(?P<version>(?:\d+?\.\d+?[p]?\d+?))", re.I)
# ]


# SERVICE_TYPE = "ssh"
# SERVICE_CLASS = "active"
# ACTION_CLASS = "analyze"


# class CSshService(CPluginBase):

#     mName = f'{SERVICE_TYPE}-service'
#     mTags = {SERVICE_TYPE, SERVICE_CLASS, ACTION_CLASS}

#     def __init__(self, core: CNiosCore):
#         self.mCore = core

#     def __call__(self, task: CTask):
#         tcpData: CTcpConnectResult = task.data

#         string = str(tcpData.data, "utf8")

#         for regex in regexList:
#             regexResult = regex.search(string)

#             if regexResult:
#                 regexResult.groupdict()

#                 return {
#                     "tcp-data": tcpData,
#                     f"{SERVICE_TYPE}-data": {
#                         "server": (regexResult["server"]).lower(),
#                         "version": (regexResult["version"]).lower()
#                     }
#                 }

#     def onComplete(self, results):
#         self.mCore.put(CTask("services-vulnerability-check", results, ETaskPriority.HIGH))

#     def onError(self, error):
#         logging.exception(error)