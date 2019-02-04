#-*- coding: utf-8 -*-

from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
from bottle import run, Bottle, template, static_file, response
import json
from threading import Thread


class SetEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


class CHttpApi:

    mName = "http-api"

    def __init__(self, core):
        self.mThread = Thread(target=self.__thread, name=self.mName)
        self.mCore = core
        self.server = Bottle("N.I.O.S: Api")

        self.__setUpRouting()

    def __setUpRouting(self):
        self.server.get("/", callback=self.__index)
        self.server.get("/results/<name>", callback=self.__results)
        self.server.get("/s/<static:path>", callback=self.__static)
        self.server.get("/websocket", callback=self.__websocket, apply=[websocket])

    def __thread(self):
        self.server.run(
            server=GeventWebSocketServer,
            host='localhost',
            port=8080,
            debug=True
            )

    def run(self):
        self.mThread.setDaemon(True)
        self.mThread.start()

    def stop(self):
        self.server.close()
        self.mThread.join()

    def __index(self):
        return template('www/templates/index.html', results=self.mCore.mResults)

    # def __statistics (только подсчеты определенных устройств и сервисов)

    def __results(self, name):
        response.set_header("Content-Type", "application/json")

        if name in ["all"]:
            return json.dumps(self.mCore.mResults, cls=SetEncoder)
        elif name in ["new"]:
            return json.dumps(self.mCore.mResults, cls=SetEncoder)
        return json.dumps({})

    def __static(self, static):
        return static_file(static, root='www/')

    def __websocket(self, ws):
        while True:
            msg = ws.receive()
            if msg is not None:
                ws.send(msg)
            else: break