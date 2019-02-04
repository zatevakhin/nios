#-*- coding: utf-8 -*-

import json
import logging
from copy import copy

class CJsonObjectManager:

    mConfig = {}

    def __init__(self, file: str):
        logging.debug("call %s()", __name__)

        try:
            self.mConfig = json.load(open(file))
        except Exception as e:
            raise e

    def get(self, param: str, default=None):
        # TODO: Warning if key not found, and used default value
        config = copy(self.mConfig)

        for key in param.split("."):
            config = config.get(key, default)

        return config

    def set(self, param: str, value):
        self.mConfig[param] = value