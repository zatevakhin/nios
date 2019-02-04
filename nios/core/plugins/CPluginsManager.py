#-*- coding: utf-8 -*-

import os
import logging
import importlib

from nios.core.auxiliary import exception
from nios.core.plugins.CPluginBase import CPluginBase


IGNORED_PLUGINS = [
    "__pycache__",
    "__init__"
]


class CPluginsManager(object):
    def __init__(self, core):
        logging.debug("call %s()", __name__)
        self.mCore = core
        self.mPluginsLocation = self.mCore.mConfig.get("core.plugins.location")

    def getPluginsFrom(self, directory: str):
        path = os.path.join(self.mPluginsLocation, directory)
        return self.loadPluginsFrom(path)

    @staticmethod
    def filterByTags(plugins: dict, tags: set):
        filtered = {}

        for name, plugin in plugins.items():
            intersection = plugin.tags.intersection(tags)
            if intersection and len(intersection) >= 2:
                filtered[name] = plugin

        if not filtered:
            logging.warning(f"Not enough or bad intersect ({tags})")

        return filtered

    def getPluginsListFrom(self, path: str):
        plugins = os.listdir(path)
        plugins = map(lambda x: os.path.splitext(x)[0], plugins)
        plugins = filter(lambda x: x not in IGNORED_PLUGINS, plugins)
        plugins = map(lambda x: os.path.join(path, x), plugins)
        plugins = map(lambda x: x.replace("/", '.'), plugins)
        return list(plugins)

    def loadPluginsFrom(self, path: str):
        plugins = self.getPluginsListFrom(path)
        loadedPlugins = {}

        for plugin in plugins:
            importlib.import_module(plugin)

        for plugin in CPluginBase.__subclasses__():
            if plugin.__module__ not in plugins:
                continue

            try:
                obj = plugin(core=self.mCore)

                loadedPlugins[obj.name] = obj
            except AttributeError as e:
                logging.warning(e, plugin.__name__)
            except Exception:
                logging.exception(exception())

        return loadedPlugins