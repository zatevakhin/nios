#-*- coding: utf-8 -*-

import logging

from nios.core.plugins.CPluginsManager import CPluginsManager
from nios.core.modules.CModuleBase import CModuleBase
from nios.core.CNiosCore import CNiosCore
from nios.core.CScheduler import CTask

from nios.core.data import ETaskType


class CServicesBruteforce(CModuleBase):

    def __init__(self, core: CNiosCore):
        self.mModuleTaskType = ETaskType.SERVICES_BRUTEFORCE
        self.mPlugins = core.getPlugins(self.name)
        self.mCore = core

        logging.info("%s: %s", __name__, self.mPlugins)

    def __call__(self, task: CTask):
        data: dict = task.data

        if not data:
            logging.warning(f"{__name__}: no data")
            return

        categories = data.get('categories', set())
        logging.info("%s: %s", __name__, categories)

        if categories:
            self.forwardToFilteredPlugins(task, categories)
        else:
            logging.warning(f"{__name__} no handler")

    def forwardToFilteredPlugins(self, task: CTask, tags: set):
        plugins = CPluginsManager.filterByTags(self.mPlugins, tags)

        for name, plugin in plugins.items():
            self.mCore.runPlugin(plugin.copy(), {"task": task})
