#-*- coding: utf-8 -*-


class CDataManager:

    def __init__(self):
        self.mDataObjects = {}

    def set(self, name, obj):
        self.mDataObjects[name] = obj

    def get(self, name, default=None):
        return self.mDataObjects.get(name, default)
