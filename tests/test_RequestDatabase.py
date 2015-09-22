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