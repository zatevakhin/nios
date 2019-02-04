#-*- coding: utf-8 -*-

import logging
from multiprocessing.dummy import Pool
from multiprocessing.pool import ApplyResult

from queue import Queue
from random import shuffle
from threading import Thread
from time import sleep

import iptools

from nios.core.CDataManager import CDataManager
from nios.core.CHttpApi import CHttpApi
from nios.core.CJsonObjectManager import CJsonObjectManager
from nios.core.CScheduler import CScheduler
from nios.core.data import CTask, ETaskPriority
from nios.core.data.ETaskType import ETaskType
from nios.core.exploits.CExploitsManager import CExploitsManager
from nios.core.modules.CModulesManager import CModulesManager
from nios.core.plugins.CPluginsManager import CPluginsManager


class WorkersPool(object):

    def __init__(self, numWorkers):
        self.mThreadPool: Pool = Pool(numWorkers)
        self.mLockQueue = Queue(numWorkers)

    def _waitFreeThread(self):
        while self.mLockQueue.full():
            item: ApplyResult = self.mLockQueue.get()

            if not item.ready():
                item.wait(1)

            if not item.ready():
                self.mLockQueue.put(item)

    def stop(self):
        self.mThreadPool.close()
        self.mThreadPool.terminate()
        self.mThreadPool.join()

    def deferredExecute(self, *args, **kwargs):
        self._waitFreeThread()
        result = self.mThreadPool.apply_async(*args, **kwargs)
        self.mLockQueue.put(result)


class CNiosCore(object):

    def __init__(self, config: str):
        self.mResults: list = []

        self.mData = CDataManager()
        self.mConfig = CJsonObjectManager(config)
        self.mPlugins = CPluginsManager(self)
        self.mModules = CModulesManager(self)
        self.mExploits = CExploitsManager(self)
        self.mScheduler = CScheduler(self)
        self.mHttpApi = CHttpApi(self)

        workers = self.mConfig.get('nios.scanning-workers-count', 4)
        self.mThreadPool: WorkersPool = WorkersPool(workers)

    def getPlugins(self, directory: str):
        return self.mPlugins.getPluginsFrom(directory)

    def run(self):
        ipRange = []
        # ipRange = list(iptools.IpRange('176.97.56.0/21'))
        # ipRange = list(iptools.IpRange('109.197.166.0/23'))
        # ipRange = list(iptools.IpRange('91.230.199.0/24'))
        # ipRange = list(iptools.IpRange("176.8.0.0/16"))

        # KTM
        # ipRange = list(iptools.IpRangeList(
        #     "93.76.0.0/16",
        #     "93.77.0.0/17",
        #     "93.77.128.0/19",
        #     "93.77.192.0/18",
        #     "93.78.0.0/15",
        #     "93.72.0.0/14"
        # ))

        ipRange = list(iptools.IpRangeList(
            "109.197.166.0/23",
            "176.97.56.0/21",
            "192.162.208.0/22"
        ))

        ipRange = ["176.97.58.244"]

        # ipRange = list(iptools.IpRangeList(
        #     "37.229.0.0/16",
        #     "46.118.0.0/15"
        # ))


        # "46.118.29.29", airlive
        # "46.119.190.45", unknown
        # "46.118.96.59", # zyxel giga iii
        # "37.229.8.48", # zyair

        # ipRange = [
            # "176.97.62.34",
            # "46.119.241.76",
            # "37.229.82.202",
            # "37.229.240.54",
            # "46.119.193.60",
            # "46.118.254.42",
            # "37.229.95.148",
            # "37.229.253.75",
            # "46.119.139.85",
            # "46.118.112.96",
            # "37.229.108.248",
            # "37.229.67.244",
            # "46.118.50.252",
            # "46.119.60.223",
            # "46.119.94.231",
            # "46.118.163.24",
            # "37.229.8.103",
            # "37.229.33.80",
            # "37.229.32.63",
            # "46.119.120.55",
            # "46.118.250.235",
        # ]

        # http://46.118.178.144:80 hv dvr
        # http://46.118.223.147:80
        # http://46.119.192.194

        # http://46.118.190.103/ dahua dvr

        # http://46.119.161.242/ dvr
        # http://37.229.247.37:8080/
        # http://46.118.244.196:80
        # http://46.118.192.248:80
        # http://46.118.70.127:80
        # http://46.119.123.130
        # http://46.119.231.197:80
        # http://46.119.234.85:8080

        # http://37.229.164.226:8080 ddwrt
        # http://46.119.224.55:8080
        # http://46.118.46.50:8080
        # http://37.229.104.138:8080
        # http://46.119.198.51:8080
        # http://37.229.214.14:8080

        # http://46.118.33.48:80 iis

        # http://46.119.160.249:5000

        # http://37.229.87.210:8080/ dlink share center

        # dlink
        # http://37.229.174.0:8080

        # http://46.119.23.105:80 ubnt
        # http://46.118.47.37:80 netis
        # http://46.119.235.166:8080/

        # http://37.229.242.162/ teamviwer
        # http://46.118.218.127/
        # http://46.119.123.173:80

        # http://46.119.69.250:8080 belkin
        # http://46.118.62.33:80 tl

        # http://46.118.13.2:8080/ xiaomi
        # http://46.118.46.4:80
        # http://37.229.20.56:80


        shuffle(ipRange)
        # ports = [80, 81, 82, 88, 1080, 1081, 1082, 1088, 8080, 8081, 8082, 8888]
        ports = [80, 8080, 1080]


        self.mScheduler.setHandler(self.mModules.get(ETaskType.SERVICES_DISCOVER))
        self.mScheduler.setHandler(self.mModules.get(ETaskType.SERVICES_VULNERABILITY_CHECK))
        self.mScheduler.setHandler(self.mModules.get(ETaskType.SERVICES_CATEGORIZING))
        self.mScheduler.setHandler(self.mModules.get(ETaskType.SERVICES_BRUTEFORCE))
        self.mScheduler.setHandler(self.mModules.get(ETaskType.WORK_FINISHED))

        self.mScheduler.run()
        self.mHttpApi.run()

        for ip in ipRange:
            self.put(CTask(ETaskType.SERVICES_DISCOVER, {'ip': ip, 'ports': ports}, ETaskPriority.LOW))

        while True:
            try:
                sleep(1)
            except KeyboardInterrupt:
                self.mThreadPool.stop()
                logging.debug("%s: %s", __name__, "self.mThreadPool.stop()")
                self.mHttpApi.stop()
                logging.debug("%s: %s", __name__, "self.mHttpApi.stop()")
                self.mScheduler.stop()
                logging.debug("%s: %s", __name__, "self.mScheduler.stop()")
                return

    def saveResult(self, data: dict):
        print("*" * 80)
        print(data)
        self.mResults.append(data)

    def put(self, task: CTask):
        self.mScheduler.put(task)

    def runPlugin(self, plugin, kwargs: dict):
        self.mThreadPool.deferredExecute(
            plugin,
            error_callback=plugin.onError,
            callback=plugin.onComplete,
            kwds=kwargs,
        )
