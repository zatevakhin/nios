# -*- coding: utf-8 -*-

import logging
from queue import PriorityQueue
from threading import Thread

from nios.core.data import CTask


class CScheduler(object):

    def __init__(self, core):
        self.mTasks = PriorityQueue()
        self.mHandlers = {}
        self.mWorking = True
        self.mThread = Thread(target=self.thread, name="scheduler")

    def run(self):
        logging.debug("%s: %s", __name__, self.mHandlers)
        self.mThread.setDaemon(True)
        self.mThread.start()

    def stop(self):
        self.mWorking = False
        self.mThread.join()

    def thread(self):
        while True:
            if not self.mWorking:
                break

            task = self.mTasks.get()

            if task.type not in self.mHandlers:
                continue

            self.mHandlers[task.type](task)

    def setHandler(self, func: object):
        self.mHandlers[func.type] = func

    def put(self, task: CTask):
        self.mTasks.put(task)
