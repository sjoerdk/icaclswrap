==============
icaclswrap
==============


.. image:: https://img.shields.io/pypi/v/icaclswrap.svg
        :target: https://pypi.python.org/pypi/icaclswrap

.. image:: https://img.shields.io/travis/sjoerdk/icaclswrap.svg
        :target: https://travis-ci.org/sjoerdk/icaclswrap

.. image:: https://readthedocs.org/projects/icacls-wrapper/badge/?version=latest
        :target: https://icacls-wrapper.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/sjoerdk/icaclswrap/shield.svg
     :target: https://pyup.io/repos/github/sjoerdk/icaclswrap/
     :alt: Updates



Windows ACL permissions management through wrapping calls to icacls windows executable


* Free software: MIT license
* Documentation: https://icacls-wrapper.readthedocs.io.


Features
--------

* Call windows executable 'icacls' to set persmissions with windows access control lists
* Wraps calls as python functions, return values as python objects and exceptions
* Downside: only works with access to the windows 'icacls' command, on a windows machine

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
