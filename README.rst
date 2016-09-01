.. contents:: Table of Contents


Introduction
============

This package implements some magical improvements compared to the default plone copy/move/rename implementation.

As far as we manage to get changes in to Plone/CMFCore this packages is no longer necessary.



Lighting fast move/rename
--------------------------
This package provides a improved move/rename implementation.
The more files you want to move the faster it will be compared to the default Plone implementation.

Basically it does not an uncatalog an afterwards a catalog of the obejct, but updates
the indexed data where necessary. This saves us from reindexing the whole moved
structure.
The main issue was that the searchableText from Files was indexed again.


Example measurement with 1 Folder, which contains 1 Document and 300 Files (almost empty PDFs):

Plone: approx. 80s
With this package: approx. 8s

PR for this change is open at: XXX (Add URL to PR)





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

**Fix inconsistent state:**

Without this patch, copy / paste could lead to incosinstent state.
When you've installed ``ftw.copymovepatches`` on an existing installation
you should visit the view ``copymovepatches-catalog-fixes`` on the site root
and run the fixes when proposed.


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
