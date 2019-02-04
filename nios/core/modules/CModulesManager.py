#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import logging
import importlib

from .CModuleBase import CModuleBase

from nios.core.auxiliary import exception
from nios.core.data import ETaskType

IGNORED_MODULES = [
    "__pycache__",
    "__init__"
]

class CModulesManager:

    def __init__(self, core):
        logging.debug("call %s()", __name__)
        self.mCore = core
        self.mModules = {}
        self.mLocation = self.mCore.mConfig.get("core.modules.location")

        self.loadModules()

    def get(self, taskType: ETaskType):
        return self.mModules.get(str(taskType.name).replace("_", "-").lower(), None)

    def getModulesList(self):
        modules = os.listdir(self.mLocation)
        modules = map(lambda x: os.path.splitext(x)[0], modules)
        modules = filter(lambda x: x not in IGNORED_MODULES, modules)
        modules = map(lambda x: os.path.join(self.mLocation, x), modules)
        modules = map(lambda x: x.replace("/", '.'), modules)
        return list(modules)

    def loadModules(self):
        modules = self.getModulesList()

        for module in modules:
            importlib.import_module(module)

        for module in CModuleBase.__subclasses__():

            obj = module(core=self.mCore)

            try:
                self.mModules[obj.name] = obj
                logging.debug("Module '%s' is loaded as '%s' in modules manager",
                                module.__name__, obj.name)

            except AttributeError as e:
                logging.warning(e, module.__name__)
            except Exception:
                logging.exception(exception())

