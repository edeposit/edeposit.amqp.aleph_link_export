#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import time
import shelve
import os.path
from contextlib import contextmanager


# Functions & classes =========================================================
@contextmanager
def shelver(fn):
    """
    In python 2.7, there is no context manager for shelve. So this is it.
    """
    db = shelve.open(fn)
    yield db
    db.close()


class ShelveDatabase(object):
    """
    Class that can save and load itself to shelve.
    """
    def __init__(self, log_fn, db_fn, db_key, logging):
        self.db_fn = db_fn  #: Path to the database file.
        self.log_fn = log_fn  #: Path to the log file.
        self.logging = logging  #: Is the logging enabled?
        self._db_key = db_key  #: Key used to load the object from shelve.

    def log(self, msg):
        """
        Log the message to the log.

        Args:
            msg (str): Message which should be logged.
        """
        if not self.logging:
            return

        # TODO: use logging backend
        msg = time.strftime("[%Y.%m.%d %H:%M:%S] ") + msg.strip() + "\n"
        with open(self.log_fn, "a") as f:
            f.write(msg)

    def save(self):
        """
        Save this object to shelve.
        """
        # save this object to database
        with shelver(self.db_fn) as db:
            db[self._db_key] = self

    def _from_obj(self, obj):
        """
        Load content of all properties from another :class:`RequestDatabase`
        object.

        Args:
            obj (obj): :class:`RequestDatabase` instance.
        """
        for key in self.__dict__.keys():
            if hasattr(obj, key):
                self.__dict__[key] = getattr(obj, key)

    def _update_self(self):
        """
        Update yourself to newest version of object in shelve.
        """
        if os.path.exists(self.db_fn):
            with shelver(self.db_fn) as db:
                self._from_obj(db[self._db_key])
                db[self._db_key] = self

    @staticmethod
    def load(fn, db_key, creator):
        """
        Load the database from the shelve `fn`.

        Args:
            fn (str): Path to the database file.
            db_key (str): What database key to use. Default
                   :attr:`.DATABASE_KEY`.
            creator (reference): Reference to the function, which will
                    create new :class:`.RequestDatabase` if the old is not
                    found. Default lambda, which expects `fn` parameter
                    ``lambda fn: ..``.

        Returns:
            obj: :class:`.RequestDatabase` instance from the `fn` or newly
                 created.
        """
        if not os.path.exists(fn):
            return creator(fn)

        with shelver(fn) as db:
            obj = db.get(db_key, None)

        if not obj:
            return creator(fn)

        obj._update_self()
        return obj
