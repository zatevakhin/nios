# -*- coding: utf-8 -*-

from enum import Enum, auto


class EServiceType(Enum):

    ROUTER = auto()
    NAS = auto()
    DVR = auto()
    SERVER = auto()
    UNKNOWN = auto()
