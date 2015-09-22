#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import shelve
import os.path
from contextlib import contextmanager

import xmltodict

from settings import LOG_PATH
from settings import REQUEST_DIR
from settings import RESPONSE_DIR
from settings import DATABASE_KEY
from settings import DATABASE_PATH

from structures import LinkUpdateResponse


# Functions & classes =========================================================
@contextmanager
def shelver(fn):
    """
    In python 2.7, there is no context manager for shelve. So this is it.
    """
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

    def log(self, msg):
        """
        Log the message to the log.

        Args:
            msg (str): Message which should be logged.
        """
        msg = msg.strip() + "\n"

        with open(self.log_path, "a") as f:
            f.write(msg)

    def add_request(self, request):
        """
        Add new `request` object to database.

        Args:
            request (obj): Object with defined :attr:`session_id` property and
                    :meth:`to_xml_dict` method.
        """
        self._req_queue[request.session_id] = request

        self.log(
            "Received request session_id(%s): %s" % (
                request.session_id,
                repr(request)
            )
        )

    def _add_response(self, response):
        self._resp_queue.append(response)

        if response.session_id in self._req_queue:
            del self._req_queue[response.session_id]

        self.log("Received response session_id(%s)." % response.session_id)

    def _process_responses(self):
        if not os.path.exists(self.resp_path):
            self.log(
                "._process_responses() called, "
                "but '%s' doesn't exists!" % self.resp_path
            )
            return

        with open(self.resp_path) as resp_f:
            xml = resp_f.read()

        xdom = xmltodict.parse(xml)

        results = xdom.get("results", {}).get("result", [])
        if type(results) not in [list, tuple]:
            results = [results]

        for result in results:
            # to allow ** creation of namedtuple
            result["session_id"] = result["@session_id"]
            del result["@session_id"]

            self._add_response(LinkUpdateResponse(**result))

    def get_responses(self):
        self._process_responses()

        session_ids = ", ".join(
            resp.session_id
            for resp in self._resp_queue
        )

        if session_ids:
            self.log("Sent back responses for: session_id(%s)." % session_ids)
        else:
            self.log(".get_repsponses(): No requests returned.")

        responses = self._resp_queue
        self._resp_queue = []

        return responses

    def to_xml(self):
        return xmltodict.unparse(
            {"records": self._req_queue if self._req_queue else None},
            pretty=True
        )

    def save(self):
        """
        Read the response XML, process it, save the database and request XML.
        """
        # write request XML
        with open(self.req_path, "w") as req_f:
            req_f.write(self.to_xml())

        # save this object to database
        with shelver(self.db_path) as db:
            db[self._db_key] = self

    @staticmethod
    def load(fn=DATABASE_PATH, db_key=DATABASE_KEY,
             creator=lambda fn: RequestDatabase(db_path=fn)):
        """
        Load the database from the shelve `fn`.

        Args:
            fn (str): Path to the database file. Default
                      :attr:`.DATABASE_PATH`.
            db_key (str): What database key to use. Default
                   :attr:`.DATABASE_KEY`.
            creator (fn reference): Reference to the function, which will
                    create new :class:`.RequestDatabase` if the old is not
                    found. Default lambda, which expects `fn` parameter
                    ``lambda fn: ..``.

        Returns:
            obj: :class:`.RequestDatabase` instance from the `fn` or newly
                 created.
        """
        with shelver(fn) as db:
            obj = db.get(db_key, None)

        if obj:
            return obj

        return creator(fn)
