#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
Module is containing all necessary global variables for the package.

Module also has the ability to read user-defined data from two paths:

- ``$HOME/_SETTINGS_PATH``
- ``/etc/_SETTINGS_PATH``

See :attr:`_SETTINGS_PATH` for details.

Note:
    If the first path is found, other is ignored.

Example of the configuration file (``$HOME/edeposit/aleph_export.json``)::

    {
        "REQUEST_FN": "/home/whatever/req.xml"
    }

Attributes
----------
"""
# Imports =====================================================================
import os
import json
import os.path


# Module configuration ========================================================

#: Path to the dir with zeo.conf and zeo_client.conf.
_BASE_PATH = "/home/aleph_export"

#: Path to the XML file, where the requests will be stored.
REQUEST_FN = os.path.join(_BASE_PATH, "edep2aleph/requests.xml")

#: Path to the file, where the Aleph will put the XML responses.
RESPONSE_FN = os.path.join(_BASE_PATH, "aleph2edep/responses.xml")

#: Path to the internal database file, which is used to store records before
#: they are serialized to XML.
DATABASE_FN = os.path.join(_BASE_PATH, "request_datase.shelve")  #:

#: Path to the file, where the logs will be stored.
LOG_FN = os.path.join(_BASE_PATH, "link_export.log")

#: Don't change this! Key for the database.
DATABASE_KEY = "request_database"

#: Link to the export XSD
EXPORT_XSD_LINK = "http://edeposit-aplikace.nkp.cz/link_export_notification.xsd"


# User configuration reader (don't edit this) =================================
_ALLOWED = [str, unicode, int, float, long, bool]  #: Allowed types.
_SETTINGS_PATH = "edeposit/aleph_export.json"  #: Path to the file.


def _get_all_constants():
    """
    Get list of all uppercase, non-private globals (doesn't start with ``_``).

    Returns:
        list: Uppercase names defined in `globals()` (variables from this \
              module).
    """
    return [
        key for key in globals().keys()
        if all([
            not key.startswith("_"),          # publicly accesible
            key.upper() == key,               # uppercase
            type(globals()[key]) in _ALLOWED  # and with type from _ALLOWED
        ])
    ]


def _substitute_globals(config_dict):
    """
    Set global variables to values defined in `config_dict`.

    Args:
        config_dict (dict): dict with data, which are used to set `globals`.

    Note:
        `config_dict` have to be dictionary, or it is ignored. Also all
        variables, that are not already in globals, or are not types defined in
        :attr:`_ALLOWED` (str, int, ..) or starts with ``_`` are silently
        ignored.
    """
    constants = _get_all_constants()

    if type(config_dict) != dict:
        return

    for key, val in config_dict.iteritems():
        if key in constants and type(val) in _ALLOWED:
            globals()[key] = val


def _read_from_paths():
    """
    Try to read data from configuration paths ($HOME/_SETTINGS_PATH,
    /etc/_SETTINGS_PATH).
    """
    home = os.environ.get("HOME", "/")
    home_path = os.path.join(home, _SETTINGS_PATH)
    etc_path = os.path.join("/etc", _SETTINGS_PATH)

    read_path = None
    if home and os.path.exists(home_path):
        read_path = home_path
    elif os.path.exists(etc_path):
        read_path = etc_path

    if read_path:
        with open(read_path) as f:
            _substitute_globals(
                json.loads(f.read())
            )


_read_from_paths()
