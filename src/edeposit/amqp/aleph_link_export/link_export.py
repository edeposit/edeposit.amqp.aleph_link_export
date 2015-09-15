#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from settings import REQUEST_DIR
from settings import RESPONSE_DIR
from settings import DATABASE_DIR

from xmltodict import unparse


# Variables ===================================================================



# Functions & classes =========================================================
class RequestDatabase(object):
    def __init__(self, req_path=REQUEST_DIR, resp_path=RESPONSE_DIR):
        self.req_path = req_path
        self.resp_path = resp_path

        self.req_queue = []
        self.resp_queue = []
        self.log = []

    def add_request(self, request):
        self.req_queue.append(request)

    def to_xml(self):
        return unparse(
            {"records": self.req_queue},
            pretty=True
        )


def export(request):
    pass


def collect_responses():
    pass
