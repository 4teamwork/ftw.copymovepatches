from ftw.builder import Builder
from ftw.builder import create
from ftw.copymovepatches.tests import FunctionalTestCase
from plone import api


class TestRenameMove(FunctionalTestCase):

    def setUp(self):
        super(TestRenameMove, self).setUp()
        self.grant('Manager')

        self.catalog = api.portal.get_tool('portal_catalog')
        self.source = create(Builder('folder'))
        self.document = create(Builder('document').within(self.source))
        self.target = create(Builder('folder'))

    def test_rid_is_the_same_after_moving(self):
        old_path = '/'.join(self.document.getPhysicalPath())
        rid = self.catalog._catalog.uids[old_path]

        # Move
        session = self.source.manage_cutObjects([self.document.getId()])
        self.target.manage_pasteObjects(session)

        new_path = '/'.join(self.target.objectValues()[0].getPhysicalPath())
        self.assertEquals(rid, self.catalog._catalog.uids[new_path])
        self.assertNotEquals(old_path, new_path)

    def test_catalog_search_by_path_after_moveing(self):
        old_path = '/'.join(self.document.getPhysicalPath())
        self.assertEquals(1, len(self.catalog(path=old_path)))

        # Move
        session = self.source.manage_cutObjects([self.document.getId()])
        self.target.manage_pasteObjects(session)

        new_path = '/'.join(self.target.objectValues()[0].getPhysicalPath())
        self.assertEquals(1, len(self.catalog(path=new_path)))

    def test_paste_object_with_same_id_already_exists(self):
        document_with_same_id = create(Builder('document').within(self.target))
        self.assertEquals(self.document.getId(), document_with_same_id.getId())

        old_path = '/'.join(self.document.getPhysicalPath())
        rid = self.catalog._catalog.uids[old_path]

        # Move
        session = self.source.manage_cutObjects([self.document.getId()])
        result = self.target.manage_pasteObjects(session)[0]

        self.assertNotEquals(result['id'], result['new_id'])

        new_path = '/'.join(self.target[result['new_id']].getPhysicalPath())
        self.assertEquals(rid, self.catalog._catalog.uids[new_path])

    def test_rid_is_the_same_after_renaming(self):
        old_path = '/'.join(self.document.getPhysicalPath())
        rid = self.catalog._catalog.uids[old_path]

        # Rename
        self.source.manage_renameObject(self.document.getId(), 'newid')

        new_path = '/'.join(self.source['newid'].getPhysicalPath())
        self.assertEquals(rid, self.catalog._catalog.uids[new_path])
        self.assertNotEquals(old_path, new_path)

    def test_catalog_search_by_path_after_renameing(self):
        old_path = '/'.join(self.document.getPhysicalPath())
        self.assertEquals(1, len(self.catalog(path=old_path)))

        # Rename
        self.source.manage_renameObject(self.document.getId(), 'newid')

        new_path = '/'.join(self.source['newid'].getPhysicalPath())
        self.assertEquals(1, len(self.catalog(path=new_path)))

    def test_crosscheck_that_copy_still_generates_a_different_rid(self):
        old_path = '/'.join(self.document.getPhysicalPath())
        rid = self.catalog._catalog.uids[old_path]

        # Copy
        session = self.source.manage_copyObjects([self.document.getId()])
        self.target.manage_pasteObjects(session)

        new_path = '/'.join(self.target.objectValues()[0].getPhysicalPath())
        self.assertNotEquals(rid, self.catalog._catalog.uids[new_path])

    def test_crosscheck_delete_still_works(self):
        old_path = '/'.join(self.source.getPhysicalPath())
        self.portal.manage_delObjects([self.source.getId()])

        self.assertFalse(len(self.catalog(path=old_path)),
                         'No longer expecting this item in the catalog')
