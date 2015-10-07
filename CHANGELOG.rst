Changelog
=========

1.2.2
-----
    - Log record updated to include whole responses.

1.2.1
-----
    - Added ability to use LinkDescription in `.document_urls` property.

1.2.0
-----
    - document_url changed to list.

1.1.0 - 1.1.4
-------------
    - Implemented option to disable logging.
    - Added ability to update itself automatically.
    - ``None`` is now returned instead of blank array, when no response is ready.
    - Added new parameter reason to output structure.

1.0.0 - 1.0.5
-------------
    - Added documentation.
    - Fixed bugs.
    - Added description.
    - Small change in docs config.
    - XSD added to XML output.
    - Fixed XML mess.
    - Fixed problem with loading of the database after restart.
    - Fixed behavior, which let the response file in the directory, so it was processed over and over again.
    - Added test for input's structure interface into ``RequestDatabase.add_request()``.

0.3.0
-----
    - Added almost 100% test coverage (everything with meaning is covered).
    - Fixed a LOT of bugs.
    - Added docstrings for every member of the package.

0.2.1
-----
    - Response structure updated.

0.2.0
-----
    - Added tests.
    - Fixed bugs in import structures.

0.1.0
-----
    - Project created.
