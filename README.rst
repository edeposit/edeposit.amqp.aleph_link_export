Introduction
============

.. image:: https://badge.fury.io/py/edeposit.amqp.aleph_link_export.png
    :target: https://pypi.python.org/pypi/edeposit.amqp.aleph_link_export

.. image:: https://img.shields.io/pypi/dm/edeposit.amqp.aleph_link_export.svg
    :target: https://pypi.python.org/pypi/edeposit.amqp.aleph_link_export

.. image:: https://readthedocs.org/projects/edeposit-amqp-aleph-link-export/badge/?version=latest
    :target: http:///edeposit-amqp-aleph-link-export.rtfd.org/

.. image:: https://img.shields.io/pypi/l/edeposit.amqp.aleph_link_export.svg

.. image:: https://img.shields.io/github/issues/edeposit/edeposit.amqp.aleph_link_export.svg
    :target: https://github.com/edeposit/edeposit.amqp.aleph_link_export/issues

Two-way communication subsystem used for updating the E-deposit_ links in Aleph.

Links created in Aleph cannot be changed automatically by direct-manipulation, so this project defines AMQP_ to XML protocol bridge. XML then copied over SCP to Aleph, processed and resulting XML response is then translated back to AMQP messages.

.. _AMQP: https://www.amqp.org/
.. _E-deposit: http://edeposit.nkp.cz/

Documentation
-------------

Full module documentation and description can be found at Read the Docs:

- http://edeposit-amqp-aleph-link-export.rtfd.org/
