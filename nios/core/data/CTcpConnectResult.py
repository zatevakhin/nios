# -*- coding: utf-8 -*-


class CTcpConnectResult(object):

    def __init__(self, ip, port):
        self.mAlive = False
        self.mData = None
        self.mException = None
        self.mIp = ip
        self.mPort = port

    @property
    def ip(self):
        return self.mIp

    @property
    def port(self):
        return self.mPort

    @property
    def alive(self):
        return self.mAlive

    @property
    def data(self):
        return self.mData

    @property
    def exception(self):
        return self.mException

    @alive.setter
    def alive(self, value):
        self.mAlive = value

    @data.setter
    def data(self, value):
        self.mData = value

    @exception.setter
    def exception(self, value):
        self.mException = value
