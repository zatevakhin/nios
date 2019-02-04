#-*- coding: utf-8 -*-

import logging

from nios.core.modules.CModuleBase import CModuleBase
from nios.core.CNiosCore import CNiosCore
from nios.core.CScheduler import CTask
from nios.core.data.ETaskType import ETaskType


class CServicesDiscover(CModuleBase):


    def __init__(self, core: CNiosCore):
        self.mModuleTaskType = ETaskType.SERVICES_DISCOVER
        self.mPlugins = core.getPlugins(self.name)
        self.mCore = core

        logging.info("%s: %s", __name__, self.mPlugins)

    def __call__(self, task: CTask):
        for _, plugin in self.mPlugins.items():
            self.mCore.runPlugin(plugin.copy(), {"task": task})
