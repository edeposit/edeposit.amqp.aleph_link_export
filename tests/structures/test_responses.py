#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest

from aleph_link_export.structures import LinkUpdateResponse


# Tests =======================================================================
def test_LinkUpdateResponse():
    lur = LinkUpdateResponse(
        status="status",
        session_id="session_id",
    )

    assert lur.status == "status"
    assert lur.session_id == "session_id"
