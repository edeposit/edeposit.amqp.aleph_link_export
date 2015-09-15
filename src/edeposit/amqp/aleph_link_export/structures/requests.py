#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from collections import namedtuple


# Requests ====================================================================
class LinkUpdateRequest(namedtuple("LinkUpdateRequest", ["uuid",
                                                         "doc_number",
                                                         "kramerius_url",
                                                         "document_url"])):
    pass


class StatusRequest(namedtuple("StatusRequest", [])):
    pass
