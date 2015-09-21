edeposit.amqp.aleph_link_export
===============================


.. _AMQP: https://www.amqp.org/
.. _bottle.py: http://bottlepy.org
.. _E-deposit: http://edeposit.nkp.cz/

Package structure
-----------------

File relations
++++++++++++++

.. image:: /_static/relations.png
    :width: 400px

API
+++

:doc:`/api/storage`:

.. toctree::
    :maxdepth: 1

    /api/archive_storage.rst
    /api/publication_storage.rst

.. toctree::
    :maxdepth: 1

    /api/api.rst
    /api/storage_handler.rst
    /api/web_tools.rst
    /api/zconf.rst
    /api/settings.rst

:doc:`/api/structures/structures`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

AMQP:

.. toctree::
    :maxdepth: 1





Database:

.. toctree::
    :maxdepth: 1




Installation
------------


AMQP protocol
-------------

Here is the list of ``Request -> Response`` pairs describing responses to AMQP communication::

TODO:

    SaveRequest.Archive -> Archive
    SaveRequest.Publication -> Publication

    SearchRequest -> SearchResult


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
This script expects that packages pytest_, fake-factory_ and sh_ is installed. In case you don't have it yet, it can be easily installed using following command::

    pip install --user pytest fake-factory sh

or for all users::

    sudo pip install pytest fake-factory sh

.. _pytest: http://pytest.org/
.. _fake-factory: https://github.com/joke2k/faker
.. _sh: https://github.com/amoffat/sh


Example
^^^^^^^



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
