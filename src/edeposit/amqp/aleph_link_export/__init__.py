#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from structures import StatusRequest
from structures import LinkDescription
from structures import LinkUpdateRequest
from structures import LinkUpdateResponse

import link_export


# Functions & classes =========================================================
def _instanceof(instance, cls):
    """
    Check type of `instance` by matching ``.__name__`` with `cls.__name__`.
    """
    return type(instance).__name__ == cls.__name__


def _send_responses(send_back):
    """
    Send back all reponses, return the last (returned things are automatically
    sent back).
    """
    responses = link_export.collect_responses()

    if not responses:
        return None

    if len(responses) == 1:
        return responses[0]

    # > 1
    for resp in responses[:-1]:
        send_back(resp)

    return responses[-1]


# Main function ===============================================================
def reactToAMQPMessage(message, send_back):
    """
    React to given (AMQP) message. `message` is expected to be
    :py:func:`collections.namedtuple` structure from :mod:`.structures` filled
    with all necessary data.

    Args:
        message (object): One of the request objects defined in
                          :mod:`.structures`.
        send_back (fn reference): Reference to function for responding. This is
                  useful for progress monitoring for example. Function takes
                  one parameter, which may be response structure/namedtuple, or
                  string or whatever would be normally returned.

    Returns:
        object: Response class from :mod:`.structures`.

    Raises:
        ValueError: if bad type of `message` structure is given.
    """
    if _instanceof(message, LinkUpdateRequest):
        link_export.export(message)

        return _send_responses(send_back)

    elif _instanceof(message, StatusRequest):
        return _send_responses(send_back)

    raise ValueError("'%s' is unknown type of request!" % str(type(message)))
