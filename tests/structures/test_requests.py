#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest

from aleph_link_export.structures import StatusRequest
from aleph_link_export.structures import LinkUpdateRequest


# Fixtures ====================================================================
@pytest.fixture
def link_update_req():
    return LinkUpdateRequest(
        uuid="uuid",
        doc_number="doc_number",
        urn_nbn="urn_nbn",
        document_url="document_url",
        kramerius_url="kramerius_url",
        session_id="session_id",
    )


@pytest.fixture
def status_request():
    return StatusRequest()


# Tests =======================================================================
def test_LinkUpdateRequest_init(link_update_req):
    assert link_update_req.uuid == "uuid"
    assert link_update_req.doc_number == "doc_number"
    assert link_update_req.urn_nbn == "urn_nbn"
    assert link_update_req.document_url == "document_url"
    assert link_update_req.kramerius_url == "kramerius_url"
    assert link_update_req.session_id == "session_id"


def test_LinkUpdateRequest_init_without_kramerius():
    lur = LinkUpdateRequest(
        uuid="uuid",
        doc_number="doc_number",
        document_url="document_url",
        session_id="session_id",
    )

    assert lur.uuid == "uuid"
    assert lur.doc_number == "doc_number"
    assert lur.document_url == "document_url"
    assert lur.session_id == "session_id"
    assert lur.kramerius_url is None
    assert lur.urn_nbn is None


def test_LinkUpdateRequest_to_dict_xml(link_update_req):
    xml_dict = link_update_req.to_dict_xml()

    assert xml_dict["@session_id"] == link_update_req.session_id
    assert xml_dict["uuid"] == link_update_req.uuid
    assert xml_dict["doc_number"] == link_update_req.doc_number
    assert xml_dict["urn_nbn"] == link_update_req.urn_nbn
    assert xml_dict["kramerius_url"] == link_update_req.kramerius_url
    assert xml_dict["document_url"] == link_update_req.document_url


def test_LinkUpdateRequest_to_dict_xml_without_kramerius_and_urn(link_update_req):
    lur = LinkUpdateRequest(
        uuid="uuid",
        doc_number="doc_number",
        document_url="document_url",
        session_id="session_id",
    )
    xml_dict = lur.to_dict_xml()

    assert xml_dict["@session_id"] == link_update_req.session_id
    assert xml_dict["uuid"] == link_update_req.uuid
    assert xml_dict["doc_number"] == link_update_req.doc_number
    assert "kramerius_url" not in xml_dict
    assert "urn_nbn" not in xml_dict
    assert xml_dict["document_url"] == link_update_req.document_url


def test_status_request(status_request):
    assert status_request == StatusRequest()
