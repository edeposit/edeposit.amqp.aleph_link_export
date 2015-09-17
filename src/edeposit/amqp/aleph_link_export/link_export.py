#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import shelve
from contextlib import contextmanager

import xmltodict

from settings import LOG_PATH
from settings import REQUEST_DIR
from settings import RESPONSE_DIR
from settings import DATABASE_KEY
from settings import DATABASE_PATH

from structures import LinkUpdateResponse


# Variables ===================================================================
# Functions & classes =========================================================
# in 2.7, there is no context manager for shelve :S
@contextmanager
def shelver(fn):
    db = shelve.open(fn)
    yield db
    db.close()


class RequestDatabase(object):
    def __init__(self, req_path=REQUEST_DIR, resp_path=RESPONSE_DIR,
                 log_path=LOG_PATH, db_path=DATABASE_PATH,
                 db_key=DATABASE_KEY):
        self.db_path = db_path
        self.log_path = log_path
        self.req_path = req_path
        self.resp_path = resp_path

        self._db_key = db_key

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

    def _process_responses(self, xml):
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

    def save(self):
        with open(self.resp_path) as resp_f:
            xml = resp_f.read()
        self._process_responses(xml)

        # write request XML
        with open(self.req_path) as req_f:
            req_f.write(self.to_xml)

        # save this object to database
        with shelver(self.db_path) as db:
            db[self._db_key] = self

    @staticmethod
    def load(fn=DATABASE_PATH, db_key=DATABASE_KEY):
        with shelver(fn) as db:
            obj = db.get(db_key, None)

        if obj:
            return obj

        return RequestDatabase(db_path=fn)


def export(request):
    pass


def collect_responses():
    pass


if __name__ == '__main__':
    rd = RequestDatabase()
    print rd.to_xml()
