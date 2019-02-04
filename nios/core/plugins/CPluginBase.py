#!/usr/bin/python
#-*- coding: utf-8 -*-

from copy import copy


class CPluginBase(object):

    def __init__(self, **kwargs):
        self.mName = None
        self.mTags = set()

    @property
    def name(self):
        if not self.mName:
            raise AttributeError("In class '%s' attribute 'mName' is not set")
        return self.mName

    @property
    def tags(self):
        return self.mTags

    def __call__(self, task):
        raise NotImplementedError

    def isAccept(self, task):
        raise NotImplementedError

    def onComplete(self, *args, **kwargs):
        raise NotImplementedError

    def onError(self, *args, **kwargs):
        raise NotImplementedError

    def copy(self):
        return copy(self)
