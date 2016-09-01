.. contents:: Table of Contents


Introduction
============

### INTRODUCTION ###


Backport of dexterity patch: set copy flags
-------------------------------------------

**Problem:**

When copying a DX container which has AT children, the UID of the AT
children was not updated.
The reason for the error is that the DX container copy did not have the
`_v_is_cp` flag while the AT children were processed and thus the flag
was not properly delegated.

**Solution:**

By copying the `_v_is_cp` and `_v_cp_refs flags` to the copy we have the
same behavior as it used to be with AT, which does fix the error.

- Issue: https://github.com/plone/Products.CMFPlone/issues/1735
- Plone 4 fix: https://github.com/plone/plone.dexterity/pull/60
- Plone 5 fix: https://github.com/plone/plone.dexterity/pull/61


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
