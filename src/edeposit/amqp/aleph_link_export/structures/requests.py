#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from collections import namedtuple

from odictliteral import odict


# Requests ====================================================================
class LinkUpdateRequest(namedtuple("LinkUpdateRequest", ["uuid",
                                                         "doc_number",
                                                         "document_url",
                                                         "kramerius_url"])):
    def __new__(cls, uuid, doc_number, document_url, kramerius_url=None):
        return super(LinkUpdateRequest, cls).__new__(
            cls,
            uuid,
            doc_number,
            document_url,
            kramerius_url
        )

    def to_dict_xml(self):
        record = odict[
            "record": odict[
                "uuid": self.uuid,
                "doc_number": self.doc_number,
                "kramerius_url": self.kramerius_url,
                "document_url": self.document_url,
            ]
        ]

        if not self.kramerius_url:
            del record["record"]["kramerius_url"]

        return record


class StatusRequest(namedtuple("StatusRequest", [])):
    pass
