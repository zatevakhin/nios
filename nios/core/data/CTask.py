# -*- coding: utf-8 -*-

from nios.core.data import ETaskType


class CTask(object):

    def __init__(self, task: ETaskType, data: dict, priority: int):
        self.mPriority = priority
        self.mVisitedPlugins = {}
        self.mType = task
        self.mData = data

    def __lt__(self, value):
        return self.mPriority < value.priority

    @property
    def priority(self):
        return self.mPriority

    @priority.setter
    def priority(self, value):
        self.mPriority = value

    @property
    def type(self):
        return self.mType

    @type.setter
    def type(self, value):
        self.mType = value

    @property
    def data(self):
        return self.mData

    @data.setter
    def data(self, value):
        self.mData = value

    @property
    def tags(self):
        return set(map(lambda x: str(x).lower(), self.mData.get("collected", dict()).values()))