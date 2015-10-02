edeposit.amqp.aleph_link_export
===============================

Two-way communication system used to deliver update requests from E-deposit_ to Aleph used in Czech National library. Updates may contain new http links to other systems or identifiers, like URN:NBN, or UUID.

Links created in Aleph cannot be changed automatically by direct-manipulation, so this project defines AMQP_ to XML protocol bridge. XML then copied over SCP to Aleph, processed and resulting XML response is then translated back to AMQP messages received by E-deposit.

.. _AMQP: https://www.amqp.org/
.. _bottle.py: http://bottlepy.org
.. _E-deposit: http://edeposit.nkp.cz/

Package structure
-----------------

File relations
++++++++++++++

.. image:: /_static/relations.png


API
+++

:doc:`/api/aleph_link_export`:

.. toctree::
    :maxdepth: 1

    /api/link_export.rst
    /api/request_database.rst
    /api/shelvedb.rst

.. toctree::
    :maxdepth: 1

    /api/settings.rst


:doc:`/api/structures/structures`:

.. toctree::
    :maxdepth: 1

    /api/structures/requests.rst
    /api/structures/responses.rst


:doc:`/notes/protocol_notes`


AMQP protocol
-------------

Here is the list of ``Request -> Response`` pairs describing responses to AMQP communication::

    LinkUpdateRequest ---> 0-N × LinkUpdateResponse
    StatusRequest -------> 0-N × LinkUpdateResponse

Protocol is really simple - you can send the :class:`.LinkUpdateRequest` and
you will get back all waiting :class:`.LinkUpdateResponse` responses. If there is none, you won't get any.

You can also trigger the lookup for waiting responses by sending periodic :class:`.StatusRequest` messages.


Installation
------------
Module is `hosted at PYPI <https://pypi.python.org/pypi/edeposit.amqp.aleph_link_export>`_,
and can be easily installed using `PIP`_::

    sudo pip install edeposit.amqp.aleph_link_export

.. _PIP: http://en.wikipedia.org/wiki/Pip_%28package_manager%29

Don't forget to add proper paths into your configuration file (see :mod:`.settings` for details) in ``/home/edeposit/aleph_export.json`` or ``/etc/edeposit/aleph_export.json``.

Example::

    {
            "REQUEST_FN": "/home/aleph_export/edep2aleph.xml",
            "RESPONSE_FN": "/home/aleph_export/aleph2edep.xml",
            "DATABASE_FN": "/home/aleph_export/database.shelve",
            "LOG_FN": "/home/aleph_export/log.txt"
    }

Warning:
    The directories have to be created before you try to run the project!

Source code
+++++++++++
Project is released under the MIT license. Source code can be found at GitHub:

- https://github.com/edeposit/edeposit.amqp.aleph_link_export

Unittests
+++++++++

Almost every feature of the project is tested by unittests. You can run those
tests using provided ``run_tests.sh`` script, which can be found in the root
of the project.

If you have any trouble, just add ``--pdb`` switch at the end of your ``run_tests.sh`` command like this: ``./run_tests.sh --pdb``. This will drop you to `PDB`_ shell.

.. _PDB: https://docs.python.org/2/library/pdb.html

Requirements
^^^^^^^^^^^^
This script expects that package pytest_ is installed. In case you don't have it yet, it can be easily installed using following command::

    pip install --user pytest

or for all users::

    sudo pip install pytest

.. _pytest: http://pytest.org/
.. _fake-factory: https://github.com/joke2k/faker
.. _sh: https://github.com/amoffat/sh


Example
^^^^^^^

::

    $ ./run_tests.sh 
    ============================= test session starts ==============================
    platform linux2 -- Python 2.7.6 -- py-1.4.30 -- pytest-2.7.2
    rootdir: /home/bystrousak/Plocha/Dropbox/c0d3z/prace/edeposit.amqp.aleph_link_export, inifile: 
    plugins: cov
    collected 17 items 

    tests/test_RequestDatabase.py .......
    tests/test_amqp_chain.py ....
    tests/structures/test_requests.py .....
    tests/structures/test_responses.py .

    ========================== 17 passed in 0.25 seconds ===========================


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
