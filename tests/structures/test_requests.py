#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest

from aleph_link_export.structures import LinkUpdateRequest


# Fixtures ====================================================================
@pytest.fixture
def link_update_req():
    return LinkUpdateRequest(
        uuid="uuid",
        doc_number="doc_number",
        document_url="document_url",
        kramerius_url="kramerius_url",
        session_id_="session_id_",
    )


# Tests =======================================================================
def test_LinkUpdateRequest_init(link_update_req):
    assert link_update_req.uuid == "uuid"
    assert link_update_req.doc_number == "doc_number"
    assert link_update_req.document_url == "document_url"
    assert link_update_req.kramerius_url == "kramerius_url"
    assert link_update_req.session_id_ == "session_id_"


def test_LinkUpdateRequest_init_without_kramerius():
    lur = LinkUpdateRequest(
        uuid="uuid",
        doc_number="doc_number",
        document_url="document_url",
        session_id_="session_id_",
    )

    assert lur.uuid == "uuid"
    assert lur.doc_number == "doc_number"
    assert lur.document_url == "document_url"
    assert lur.session_id_ == "session_id_"
    assert lur.kramerius_url is None
