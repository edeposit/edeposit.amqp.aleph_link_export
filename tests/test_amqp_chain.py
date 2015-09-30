#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import shutil
import os.path
import tempfile

import pytest

import aleph_link_export.link_export
from aleph_link_export import StatusRequest
from aleph_link_export import LinkUpdateRequest
from aleph_link_export import LinkUpdateResponse
from aleph_link_export import reactToAMQPMessage
from aleph_link_export.request_database import RequestDatabase

from test_RequestDatabase import RESPONSE_STR
from test_RequestDatabase import THREE_RESPONSES_STR
from structures.test_requests import link_update_req


# Variables ===================================================================
TMP_DIR = None


# Setup =======================================================================
def setup_module(module):
    global TMP_DIR
    TMP_DIR = tempfile.mkdtemp()

    aleph_link_export.link_export.REQUEST_DATABASE = RequestDatabase(
        req_fn=os.path.join(TMP_DIR, "requests.xml"),
        resp_fn=os.path.join(TMP_DIR, "responses.xml"),
        log_fn=os.path.join(TMP_DIR, "log.txt"),
        db_fn=os.path.join(TMP_DIR, "database.shelve"),
    )


def teardown_module(module):
    shutil.rmtree(TMP_DIR)


# Tests =======================================================================
def test_export(link_update_req):
    aleph_link_export.link_export.export(link_update_req)

    assert os.path.exists(os.path.join(TMP_DIR, "requests.xml"))
    with open(os.path.join(TMP_DIR, "requests.xml")) as f:
        data = f.read()

    assert "<records x" in data
    sess = '<record session_id="%s">' % link_update_req.session_id
    assert sess in data


def test_link_update_request(link_update_req):
    DB = []

    assert reactToAMQPMessage(link_update_req, lambda x: DB.append(x)) is None
    assert reactToAMQPMessage(link_update_req, lambda x: DB.append(x)) is None

    assert DB == []
    assert reactToAMQPMessage(StatusRequest(), lambda x: DB.append(x)) is None


def test_link_status_request():
    with open(os.path.join(TMP_DIR, "responses.xml"), "w") as f:
        f.write(THREE_RESPONSES_STR)

    DB = []
    resp = reactToAMQPMessage(StatusRequest(), lambda x: DB.append(x))

    assert len(DB) == 2

    assert DB[0].session_id == "aaa"
    assert DB[0].status == "OK"

    assert DB[1].session_id == "bbb"
    assert DB[1].status == "OK"

    assert resp.session_id == "ccc"
    assert resp.status == "ERROR"


def test_one_link_status_request():
    with open(os.path.join(TMP_DIR, "responses.xml"), "w") as f:
        f.write(RESPONSE_STR)

    DB = []
    resp = reactToAMQPMessage(StatusRequest(), lambda x: DB.append(x))

    assert not DB

    assert resp.session_id == "session_id"
    assert resp.status == "OK"

    # test that the queue was cleaned
    DB = []
    resp = reactToAMQPMessage(StatusRequest(), lambda x: DB.append(x))

    assert not DB
    assert not resp