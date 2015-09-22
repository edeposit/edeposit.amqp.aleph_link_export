#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from settings import LOG_FN
from settings import REQUEST_FN
from settings import RESPONSE_FN
from settings import DATABASE_KEY
from settings import DATABASE_FN

from request_database import RequestDatabase


# Variables ===================================================================
REQUEST_DATABASE = RequestDatabase(
    req_fn=REQUEST_FN,
    resp_fn=RESPONSE_FN,
    log_fn=LOG_FN,
    db_fn=DATABASE_FN,
    db_key=DATABASE_KEY,
)


# Functions & classes =========================================================
def export(request):
    """
    Save the export `request` to the database.

    Args:
        request (obj): Instance of :class:`.LinkUpdateRequest`.
    """
    REQUEST_DATABASE.add_request(request)
    REQUEST_DATABASE.save()


def collect_responses():
    """
    Collect processed resposes.

    Returns:
        list: List of :class:`.LinkUpdateResponse` objects.
    """
    resp = REQUEST_DATABASE.get_responses()
    REQUEST_DATABASE.save()

    return resp
