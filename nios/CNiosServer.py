#-*- coding: utf-8 -*-

import logging

from nios.core.CNiosCore import CNiosCore
import coloredlogs


coloredlogs.install(
    level='DEBUG',
    milliseconds=True,
    fmt='[%(asctime)s.%(msecs)03d][%(threadName)s][%(levelname)-8s](%(filename)s:%(lineno)d) %(message)s'
    )

def main():
    core = CNiosCore("config/nios.json")
    core.run()

# from http.server import HTTPServer, BaseHTTPRequestHandler
# from socketserver import ThreadingMixIn


# class ThreadedHttpServer(ThreadingMixIn, HTTPServer):
#     """Handle requests in a separate thread."""


# class CNiosServer(BaseHTTPRequestHandler):
#     pass
