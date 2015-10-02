#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os.path

import xmltodict

from settings import LOG_FN
from settings import REQUEST_FN
from settings import RESPONSE_FN
from settings import DATABASE_FN
from settings import DATABASE_KEY
from settings import EXPORT_XSD_LINK
from settings import LOGGING_ENABLED

from shelvedb import ShelveDatabase
from structures import LinkUpdateResponse


# Classes =====================================================================
class RequestDatabase(ShelveDatabase):
    """
    Keep the track of requests and resposes and their serialization and
    deserialization from/to XMl.
    """
    def __init__(self,
                 log_fn=LOG_FN,
                 db_fn=DATABASE_FN,
                 db_key=DATABASE_KEY,
                 logging=LOGGING_ENABLED,
                 req_fn=REQUEST_FN,
                 resp_fn=RESPONSE_FN,
                 xsd_url=EXPORT_XSD_LINK):
        super(RequestDatabase, self).__init__(
            log_fn=log_fn,
            db_fn=db_fn,
            db_key=db_key,
            logging=logging,
        )

        self.req_fn = req_fn  #: Path to the request XML.
        self.resp_fn = resp_fn  #: Path to the response XML
        self.xsd_url = xsd_url

        self._req_queue = {}
        self._resp_queue = []

    def add_request(self, request):
        """
        Add new `request` object to database.

        Args:
            request (obj): Object with defined :attr:`session_id` property and
                    :meth:`to_dict_xml` method.
        """
        if not (hasattr(request, "session_id") and
                hasattr(request, "to_dict_xml")):
            raise ValueError(
                "Object must have .session_id property and .to_dict_xml() "
                "method!"
            )

        self._req_queue[request.session_id] = request

        self.log(
            "Received request session_id(%s): %s" % (
                request.session_id,
                repr(request)
            )
        )

    def _add_response(self, response):
        """
        Add responese from XML to the internal queue.

        Args:
            response (obj): :class:`.LinkUpdateResponse` object.
        """
        self._resp_queue.append(response)

        if response.session_id in self._req_queue:
            del self._req_queue[response.session_id]

        self.log("Received response session_id(%s)." % response.session_id)

    def _process_responses(self):
        """
        Go thru response XML (:attr:`.resp_fn`) and put them all in the
        response queue using :meth:`_add_response`.
        """
        if not os.path.exists(self.resp_fn):
            self.log(
                "._process_responses() called, "
                "but '%s' not found." % self.resp_fn
            )
            return

        with open(self.resp_fn) as resp_f:
            xml = resp_f.read()

        xdom = xmltodict.parse(xml)

        # parse XML
        results = xdom.get("results", {}).get("result", [])
        if type(results) not in [list, tuple]:
            results = [results]

        # convert XML results to LinkUpdateResponse structure
        for result in results:
            # to allow ** creation of namedtuple
            result["session_id"] = result["@session_id"]
            del result["@session_id"]

            # copy reason or set it to None
            result["reason"] = result.get("reason", None)

            self._add_response(LinkUpdateResponse(**result))

        os.unlink(self.resp_fn)
        self.log(
            "Aleph response queue processed. Got %d responses." % len(results)
        )

    def get_responses(self):
        """
        Process response queue, remove finished requests from request queue,
        return list of response objects.

        Returns:
            list: List of :class:`.LinkUpdateResponse` objects.
        """
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
        """
        Convert :attr:`_req_queue` to XML as defined in request XSD.

        Returns:
            unicode: XML.
        """
        if not self._req_queue:
            return xmltodict.unparse({"records": None}, pretty=True)

        record_dicts = [
            rec.to_dict_xml()
            for rec in self._req_queue.values()
        ]

        return xmltodict.unparse(
            {
                "records": {
                    "record": record_dicts,
                    "@xsi:schemaLocation": self.xsd_url,
                    "@xmlns": self.xsd_url.replace(".xsd", ""),
                    "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                }
            },
            pretty=True
        )

    def save(self):
        """
        Read the response XML, process it, save the database and request XML.
        """
        # write request XML
        with open(self.req_fn, "w") as req_f:
            req_f.write(self.to_xml())

        super(RequestDatabase, self).save()

    @staticmethod
    def load(fn=DATABASE_FN, db_key=DATABASE_KEY,
             creator=lambda fn: RequestDatabase(db_fn=fn)):
        """
        Load the database from the shelve `fn`.

        Args:
            fn (str): Path to the database file. Default
                      :attr:`.DATABASE_FN`.
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
        return ShelveDatabase.load(creator=creator, fn=fn, db_key=db_key)
