#-*- coding: utf-8 -*-

import logging

from nios.core.modules.CModuleBase import CModuleBase
from nios.core.CNiosCore import CNiosCore
from nios.core.data import CTcpConnectResult
from nios.core.plugins.CPluginsManager import CPluginsManager
from nios.core.CScheduler import CTask
from nios.core.data.ETaskType import ETaskType

class CServicesCategorizing(CModuleBase):

    def __init__(self, core: CNiosCore):
        self.mModuleTaskType = ETaskType.SERVICES_CATEGORIZING
        self.mPlugins = core.getPlugins(self.name)
        self.mCore = core

        logging.info("%s: %s", __name__, self.mPlugins)

    def __call__(self, task: CTask):
        result: CTcpConnectResult = task.data.get("tcp")

        if result.alive:
            for name, plugin in self.mPlugins.items():
                self.mCore.runPlugin(plugin.copy(), {"task": task})
