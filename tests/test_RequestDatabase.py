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
        req_path=os.path.join(TMP_DIR, "requests.xml"),
        resp_path=os.path.join(TMP_DIR, "responses.xml"),
        log_path=os.path.join(TMP_DIR, "log.txt"),
        db_path=os.path.join(TMP_DIR, "database.shelve"),
    )

# with pytest.raises(Exception):
#     raise Exception()


# Tests =======================================================================
def test_RequestDatabase_init():
    RequestDatabase()


def test_request_database_fixture(request_database):
    assert os.path.exists(
        os.path.dirname(request_database.db_path)
    )

    request_database.save()

    assert os.path.exists(request_database.db_path)
    assert "<records>" in open(request_database.req_path).read()

    assert not request_database.get_responses()


def test_save(request_database, link_update_req):
    request_database.add_request(link_update_req)

    request_database.save()
    with open(request_database.log_path) as f:
        msg = "Received request session_id(%s)" % link_update_req.session_id
        assert msg in f.read()


def test_get_responses(request_database, link_update_req):
    request_database.add_request(link_update_req)

    with open(os.path.join(TMP_DIR, "responses.xml"), "w") as f:
        f.write(
            """<?xml version="1.0" encoding="UTF-8"?>

<results>
    <result session_id="%s">
        <status>OK</status>
    </result>
</results>""" % link_update_req.session_id
        )

    assert link_update_req.session_id in request_database._req_queue
    resp = request_database.get_responses()

    assert resp
    assert len(resp) == 1

    assert resp[0].session_id == link_update_req.session_id
    assert resp[0].status == "OK"

    assert link_update_req.session_id not in request_database._req_queue


def test_get_multiple_responses(request_database):
    with open(os.path.join(TMP_DIR, "responses.xml"), "w") as f:
        f.write(
            """<?xml version="1.0" encoding="UTF-8"?>

<results>
    <result session_id="aaa">
        <status>OK</status>
    </result>
    <result session_id="bbb">
        <status>OK</status>
    </result>
    <result session_id="ccc">
        <status>ERROR</status>
    </result>
</results>"""
        )

    resp = request_database.get_responses()

    assert resp
    assert len(resp) == 3

    assert resp[0].session_id == "aaa"
    assert resp[0].status == "OK"

    assert resp[1].session_id == "bbb"
    assert resp[1].status == "OK"

    assert resp[2].session_id == "ccc"
    assert resp[2].status == "ERROR"
