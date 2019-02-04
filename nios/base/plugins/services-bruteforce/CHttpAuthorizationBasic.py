
#-*- coding: utf-8 -*-

import logging

import requests

from nios.core.auxiliary import exception
from nios.core.CNiosCore import CNiosCore
from nios.core.data import CTask, CTcpConnectResult, ETaskPriority
from nios.core.plugins.CPluginBase import CPluginBase


SERVICE_TYPE = "http"
ACTION_CLASS = "bruteforce"


class CHttpAuthorizationBasic(CPluginBase):

    mName = f'{ACTION_CLASS}-{SERVICE_TYPE}'
    mTags = {SERVICE_TYPE, ACTION_CLASS}

    def __init__(self, core: CNiosCore):
        self.mCore = core

    def __call__(self, task: CTask):
        tcpData: CTcpConnectResult = task.data
