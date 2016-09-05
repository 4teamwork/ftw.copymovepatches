from Acquisition import aq_base
from OFS.interfaces import IObjectWillBeMovedEvent
from plone import api
from zope.container.interfaces import IObjectAddedEvent
from zope.container.interfaces import IObjectMovedEvent
from zope.lifecycleevent.interfaces import IObjectCopiedEvent
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
import inspect


"""This is the original method, we are replacing:
From https://github.com/zopefoundation/Products.CMFCore/blob/2.2.9/Products/CMFCore/CMFCatalogAware.py
Products.CMFCore 2.2.9


def handleContentishEvent(ob, event):

    if IObjectAddedEvent.providedBy(event):
        ob.notifyWorkflowCreated()
        ob.indexObject()

    elif IObjectMovedEvent.providedBy(event):
        if event.newParent is not None:
            ob.indexObject()

    elif IObjectWillBeMovedEvent.providedBy(event):
        if event.oldParent is not None:
            ob.unindexObject()

    elif IObjectCopiedEvent.providedBy(event):
        if hasattr(aq_base(ob), 'workflow_history'):
            del ob.workflow_history

    elif IObjectCreatedEvent.providedBy(event):
        if hasattr(aq_base(ob), 'addCreator'):
            ob.addCreator()

"""

"""
Basically it does not an uncatalog an afterwards a catalog, but just updates
the new path where necessary. This saves us from reindexing the whole moved
structure.
Unfortunately there are several path related indexes, which needs to be update.
But so far this change means a performance boost by factor 10.

The main issue was that the searchableText from Files was indexed again.

Messurements:
Folder with a Document and 300 simple PDF-Files:
OLD: about 80s
NEW: about 8s
"""


def handleContentishEvent(ob, event):
    """ Event subscriber for (IContentish, IObjectEvent) events.
    """
    if IObjectAddedEvent.providedBy(event):
        ob.notifyWorkflowCreated()
        ob.indexObject()

    elif IObjectMovedEvent.providedBy(event):
        if event.newParent is not None:
            rid = getattr(ob, '__rid')
            catalog = api.portal.get_tool('portal_catalog')
            _catalog = catalog._catalog

            new_path = '/'.join(ob.getPhysicalPath())
            old_path = _catalog.paths[rid]

            del _catalog.uids[old_path]
            _catalog.uids[new_path] = rid
            _catalog.paths[rid] = new_path

            ob.reindexObject(idxs=[
                'path',
                'allowedRolesAndUsers',
                'modified',
                'id',
                'getId'])

            delattr(ob, '__rid')

    elif IObjectWillBeMovedEvent.providedBy(event):
        # Move/Rename
        if event.oldParent is not None and event.newParent is not None:
            catalog = api.portal.get_tool('portal_catalog')
            ob_path = '/'.join(ob.getPhysicalPath())
            rid = catalog._catalog.uids[ob_path]

            setattr(ob, '__rid', rid)
        else:
            # Delete
            ob.unindexObject()

    elif IObjectCopiedEvent.providedBy(event):
        if hasattr(aq_base(ob), 'workflow_history'):
            del ob.workflow_history

    elif IObjectCreatedEvent.providedBy(event):
        if hasattr(aq_base(ob), 'addCreator'):
            ob.addCreator()


def marmoset_patch(old, new, extra_globals={}):
    g = old.func_globals
    g.update(extra_globals)
    c = inspect.getsource(new)
    exec c in g

    old.func_code = g[new.__name__].func_code


def apply_patch(scope, original, replacement):
    marmoset_patch(scope.handleContentishEvent,
                   replacement,
                   {'api': api})
