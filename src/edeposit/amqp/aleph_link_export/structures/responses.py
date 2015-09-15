#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from collections import namedtuple


# Requests ====================================================================
class LinkUpdateResponse(namedtuple("LinkUpdateResponse", ["uuid",
                                                           "doc_number",
                                                           "status"])):
    pass
