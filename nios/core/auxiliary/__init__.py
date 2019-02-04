# -*- coding: utf-8 -*-

import traceback
import sys


def exception():
    return "".join(traceback.format_exception(*sys.exc_info()))
