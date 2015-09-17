#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import xmltodict

from settings import LOG_PATH
from settings import REQUEST_DIR
from settings import RESPONSE_DIR
from settings import DATABASE_DIR

from structures import LinkUpdateResponse


# Variables ===================================================================



# Functions & classes =========================================================
class RequestDatabase(object):
    def __init__(self, req_path=REQUEST_DIR, resp_path=RESPONSE_DIR,
                 log_path=LOG_PATH):
        self.req_path = req_path
        self.resp_path = resp_path
        self.log_path = log_path

        self._req_queue = {}
        self._resp_queue = []
        self._log = []

    def add_request(self, request):
        self._req_queue[request._session_id] = request

        self.log(
            "Received request session_id(%s): %s" % (
                request._session_id,
                repr(request)
            )
        )

    def _add_response(self, response):
        self._resp_queue.append(response)
        del self._req_queue[response._session_id]

        self.log("Received response session_id(%s)." % response._session_id)

    def process_responses(self, xml):
        xdom = xmltodict.parse(xml)

        for result in xdom["results"]:
            # to allow ** creation of namedtuple
            result["_session_id"] = result["@session_id"]
            del result["@session_id"]

            self._add_response(LinkUpdateResponse(**result))

    def log(self, msg):
        msg = msg.strip() + "\n"

        with open(self.log_path, "a") as f:
            f.write(msg)

    def get_responses(self):
        session_ids = ", ".join(
            resp._session_id
            for resp in self._resp_queue
        )

        self.log("Sen't back responses for: session_id(%s)." % session_ids)

        responses = self._resp_queue
        self._resp_queue = []

        return responses

    def to_xml(self):
        return xmltodict.unparse(
            {"records": self._req_queue if self._req_queue else None},
            pretty=True
        )


def export(request):
    pass


def collect_responses():
    pass


if __name__ == '__main__':
    rd = RequestDatabase()
    print rd.to_xml()
