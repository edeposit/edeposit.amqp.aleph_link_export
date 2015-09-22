#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from collections import namedtuple


# Requests ====================================================================
class LinkUpdateResponse(namedtuple("LinkUpdateResponse", ["status",
                                                           "session_id"])):
    """
    Response to the :class:`.LinkUpdateRequest` request.

    This object is returned only when the Aleph signals, that the record was
    really updated.

    Attributes:
        status (str): Status of the update request. Either ``OK``, or
                      ``ERROR``.
        session_id (str): Corresponding session id.
    """
