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

from aleph_link_export.request_database import RequestDatabase

from structures.test_requests import link_update_req


# Variables ===================================================================
TMP_DIR = None
RESPONSE_STR = """<?xml version="1.0" encoding="UTF-8"?>

<results>
    <result session_id="session_id">
        <status>OK</status>
    </result>
</results>"""

THREE_RESPONSES_STR = """<?xml version="1.0" encoding="UTF-8"?>

<results>
    <result session_id="aaa">
        <status>OK</status>
    </result>
    <result session_id="bbb">
        <status>OK</status>
    </result>
    <result session_id="ccc">
        <status>ERROR</status>
        <reason>There is reason!</reason>
    </result>
</results>"""


# Setup =======================================================================
def setup_module(module):
    global TMP_DIR
    TMP_DIR = tempfile.mkdtemp()


def teardown_module(module):
    shutil.rmtree(TMP_DIR)


# Fixtures ====================================================================
@pytest.fixture
def request_database():
    return RequestDatabase(
        req_fn=os.path.join(TMP_DIR, "requests.xml"),
        resp_fn=os.path.join(TMP_DIR, "responses.xml"),
        log_fn=os.path.join(TMP_DIR, "log.txt"),
        db_fn=os.path.join(TMP_DIR, "database.shelve"),
    )


# Tests =======================================================================
def test_RequestDatabase_init():
    RequestDatabase()


def test_request_database_fixture(request_database):
    assert os.path.exists(
        os.path.dirname(request_database.db_fn)
    )

    request_database.save()

    assert os.path.exists(request_database.db_fn)
    assert "<records>" in open(request_database.req_fn).read()

    assert not request_database.get_responses()


def test_save(request_database, link_update_req):
    request_database.add_request(link_update_req)

    request_database.save()
    with open(request_database.log_fn) as f:
        msg = "Received request session_id(%s)" % link_update_req.session_id
        assert msg in f.read()

    with open(request_database.req_fn) as f:
        data = f.read()

    assert "<records x" in data
    sess = '<record session_id="%s">' % link_update_req.session_id
    assert sess in data


def test_get_responses(request_database, link_update_req):
    request_database.add_request(link_update_req)

    with open(os.path.join(TMP_DIR, "responses.xml"), "w") as f:
        f.write(RESPONSE_STR)

    assert "session_id" in request_database._req_queue
    resp = request_database.get_responses()

    assert resp
    assert len(resp) == 1

    assert resp[0].session_id == "session_id"
    assert resp[0].status == "OK"

    assert "session_id" not in request_database._req_queue


def test_get_multiple_responses(request_database):
    with open(os.path.join(TMP_DIR, "responses.xml"), "w") as f:
        f.write(THREE_RESPONSES_STR)

    resp = request_database.get_responses()

    assert resp
    assert len(resp) == 3

    assert resp[0].session_id == "aaa"
    assert resp[0].status == "OK"
    assert not resp[0].reason

    assert resp[1].session_id == "bbb"
    assert resp[1].status == "OK"
    assert not resp[1].reason

    assert resp[2].session_id == "ccc"
    assert resp[2].status == "ERROR"
    assert resp[2].reason == "There is reason!"


def test_load_database(request_database, link_update_req):
    request_database.add_request(link_update_req)

    rd = RequestDatabase.load(fn=request_database.db_fn)
    assert rd
    assert rd.req_fn == request_database.req_fn
    assert rd._req_queue == request_database._req_queue
    assert rd._resp_queue == request_database._resp_queue


def test_load_database_creator(request_database):
    rd = RequestDatabase.load(
        fn=os.path.join(TMP_DIR, "azgabash.shelve")
    )
    assert rd
