#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from collections import namedtuple

from odictliteral import odict


# Requests ====================================================================
class LinkDescription(namedtuple("LinkDescription", ["url", "format"])):
    """
    Optional structure, which can be used instead of string to describe the
    format of the `url`.

    Attributes:
        url (str): URL of the document.
        format (str): Format of the document.
    """
    def to_dict_xml(self):
        """
        Serialize the object to dictionary, which may be later used for
        conversion to XML.

        Retruns:
            OrderedDict: Itself as ordered dict.
        """
        return odict[
            "#text": self.url,
            "@format": self.format,
        ]


class LinkUpdateRequest(namedtuple("LinkUpdateRequest", ["uuid",
                                                         "doc_number",
                                                         "document_urls",
                                                         "kramerius_url",
                                                         "urn_nbn",
                                                         "session_id"])):
    """
    Request to update metadata in Aleph.

    Attributes:
        session_id (str): Session_id for this request. Used to pair requests
                   with :mod:`.responses`.
        uuid (str): UUID for the `doc_number` you wish to update.
        doc_number (str): Document number of the document you wish to update.
                   If there is a summary aleph record for this document at
                   Aleph please send a `doc_number` of this summary aleph
                   record.
        document_urls (list): Newly added public URL to the storage / whatever
                     subsystem. List of strings or :class:`LinkDescription`.
        kramerius_url (str, default None): Newly added URL to the Kramerius
                      subsystem.
        urn_nbn (str, default None): Optional newly added URN:NBN for the
                                     record.
    """
    def __new__(cls, uuid, doc_number, document_urls, session_id, urn_nbn=None,
                kramerius_url=None):
        if type(document_urls) not in [list, tuple]:
            document_urls = [document_urls]

        return super(LinkUpdateRequest, cls).__new__(
            cls,
            uuid=uuid,
            doc_number=doc_number,
            document_urls=document_urls,
            kramerius_url=kramerius_url,
            urn_nbn=urn_nbn,
            session_id=session_id
        )

    def to_dict_xml(self):
        """
        Convert the structure to nested ordered-dicts, which are later used
        for construction of the XML.

        Returns:
            OrderedDict: Itself as ordered dicts.
        """
        # make sure, that LinkDescription instances are serialized
        document_urls = [
            doc.to_dict_xml() if isinstance(doc, LinkDescription) else doc
            for doc in self.document_urls
        ]

        record = odict[
            "@session_id": self.session_id,
            "uuid": self.uuid,
            "doc_number": self.doc_number,
            "urn_nbn": self.urn_nbn,
            "kramerius_url": self.kramerius_url,
            "document_url": document_urls,
        ]

        if not self.kramerius_url:
            del record["kramerius_url"]

        if not self.urn_nbn:
            del record["urn_nbn"]

        return record


class StatusRequest(namedtuple("StatusRequest", [])):
    """
    This structure is used to wake the daemon to go and check whether the files
    on the disc changed or not.
    """
