#-*- coding: utf-8 -*-

import logging
import socket

from nios.core.auxiliary import exception
from nios.core.CNiosCore import CNiosCore
from nios.core.data import (CTask, CTcpConnectResult, EServiceType,
                            ETaskPriority, ETaskType)
from nios.core.plugins.CPluginBase import CPluginBase


class CTcpConnect(CPluginBase):

    mName = 'tcp-connect'

    def __init__(self, core: CNiosCore):
        self.mConnectTimeout = core.mConfig.get('timeout.tcp-connect', 0.2)
        self.mReadTimeout = core.mConfig.get('timeout.tcp-connect-read', 2.0)

        self.mCore = core

    def __call__(self, task: CTask):
        ip = task.data.get("ip")
        ports = task.data.get("ports")

        aliveServices = []

        for port in ports:
            connectResult = self.executeTcpConnect(ip, port)
            if connectResult.alive:
                logging.debug(f"tcp-connect({ip}:{port}) [OK]")
                aliveServices.append(connectResult)

        return aliveServices

    def onComplete(self, results):
        for result in results:
            data = { "tcp": result, "service-type": EServiceType.UNKNOWN, "collected": {} }
            self.mCore.put(CTask(ETaskType.SERVICES_CATEGORIZING, data, ETaskPriority.NORMAL))

    def onError(self, error):
        logging.exception(error)

    def executeTcpConnect(self, ip, port):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.settimeout(self.mConnectTimeout)

        result = CTcpConnectResult(ip, port)

        try:
            connection.connect((ip, port))
            result.alive = True

            connection.settimeout(self.mReadTimeout)
            result.data = connection.recv(1024)

        except socket.timeout as e:
            result.exception = e

        except socket.error as e:
            result.exception = e

        finally:
            connection.close()

        return result
