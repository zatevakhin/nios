# -*- coding: utf-8 -*-

from enum import Enum, auto


class ETaskType(Enum):

    SERVICES_DISCOVER = auto()
    SERVICES_VULNERABILITY_CHECK = auto()
    SERVICES_CATEGORIZING = auto()
    SERVICES_BRUTEFORCE = auto()
    WORK_FINISHED = auto()
    UNKNOWN = auto()
