#!/usr/bin/python
#-*- coding: utf-8 -*-

from nios.core.data import ETaskType


class CModuleBase(object):

    def __init__(self, **kwargs):
        self.mModuleTaskType: ETaskType = ETaskType.UNKNOWN

    @property
    def name(self):
        if not self.mModuleTaskType:
            raise AttributeError("In class '%s' attribute 'mModuleTaskType' is not set")

        return str(self.mModuleTaskType.name).replace("_", "-").lower()

    @property
    def type(self):
        if not self.mModuleTaskType:
            raise AttributeError("In class '%s' attribute 'mModuleTaskType' is not set")

        return self.mModuleTaskType

    def __call__(self, **kwargs):
        raise NotImplementedError

