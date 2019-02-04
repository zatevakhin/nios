#-*- coding: utf-8 -*-

import logging

from nios.core.modules.CModuleBase import CModuleBase
from nios.core.CNiosCore import CNiosCore
from nios.core.CScheduler import CTask
from nios.core.data import ETaskType
from nios.core.data import EServiceType


class CWorkFinished(CModuleBase):

    def __init__(self, core: CNiosCore):
        self.mModuleTaskType = ETaskType.WORK_FINISHED
        self.mCore = core

    def __call__(self, task: CTask):
        data: dict = task.data

        self.mCore.saveResult(self.mergeData(data))

    def mergeData(self, data):
        result = {
            "ip": data["tcp"].ip,
            "port": data["tcp"].port,
            "http": {
                "headers": data.get("http", {}).get("headers", {}),
                "code": data.get("http", {}).get("code", None)
            },
            "bruteforce": data.get("bruteforce", {}),
            "exploit": data.get("exploit", {}),
            "collected": data.get("collected", {})
        }

        return CWorkFinished.postProcessData(result)

    @staticmethod
    def mapServiceType(serviceType: str):
        return ({
            "none": EServiceType.UNKNOWN,
            "server": EServiceType.SERVER,
            "router": EServiceType.ROUTER,
            "dvr": EServiceType.DVR,
            "nas": EServiceType.NAS,
        }).get(str(serviceType).lower(), EServiceType.UNKNOWN)

    @staticmethod
    def postProcessData(data: dict):
        collected = data.get("collected", {})
        serviceType = CWorkFinished.mapServiceType(collected.pop("type", None))
        collected.update({"type": serviceType})
        data.update({"collected": collected})
        return data
