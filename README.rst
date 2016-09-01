.. contents:: Table of Contents


Introduction
============

### INTRODUCTION ###

Compatibility
-------------

Plone 4.3.x


Installation
============

- Add the package to your buildout configuration:

::

    [instance]
    eggs +=
        ...
        ftw.copymovepatches


Usage
=====

### USAGE ###

Development
===========

**Python:**

1. Fork this repo
2. Clone your fork
3. Shell: ``ln -s development.cfg buidlout.cfg``
4. Shell: ``python boostrap.py``
5. Shell: ``bin/buildout``

Run ``bin/test`` to test your changes.

Or start an instance by running ``bin/instance fg``.


Links
=====

- Github: https://github.com/4teamwork/ftw.copymovepatches
- Issues: https://github.com/4teamwork/ftw.copymovepatches/issues
- Pypi: http://pypi.python.org/pypi/ftw.copymovepatches
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.copymovepatches


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.copymovepatches`` is licensed under GNU General Public License, version 2.
