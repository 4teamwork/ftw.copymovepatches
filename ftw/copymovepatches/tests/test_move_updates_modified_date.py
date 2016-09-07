from datetime import datetime
from DateTime import DateTime
from ftw.builder import Builder
from ftw.builder import create
from ftw.copymovepatches.tests import FunctionalTestCase
from ftw.testing import freeze
from plone import api


class TestMoveUpdatesModifiedDate(FunctionalTestCase):

    def test_moving_AT_object_updates_modified_date(self):
        self.grant('Manager')
        old_parent = create(Builder('folder').titled(u'Old Parent'))
        new_parent = create(Builder('folder').titled(u'New Parent'))

        with freeze(datetime(2000, 1, 1)) as clock:
            folder = create(Builder('folder').within(old_parent))
            self.assert_modified_date(datetime(2000, 1, 1), folder)

            clock.forward(days=4)
            new_parent.manage_pasteObjects(old_parent.manage_cutObjects(
                [folder.getId()]))
            folder = new_parent.get(folder.getId())
            self.assert_modified_date(datetime(2000, 1, 5), folder)

    def test_moving_DX_object_updates_modified_date(self):
        self.grant('Manager')
        old_parent = create(Builder('dx container').titled(u'Old Parent'))
        new_parent = create(Builder('dx container').titled(u'New Parent'))

        with freeze(datetime(2000, 1, 1)) as clock:
            folder = create(Builder('dx container').within(old_parent))
            self.assert_modified_date(datetime(2000, 1, 1), folder)

            clock.forward(days=4)
            new_parent.manage_pasteObjects(old_parent.manage_cutObjects(
                [folder.getId()]))
            folder = new_parent.get(folder.getId())
            self.assert_modified_date(datetime(2000, 1, 5), folder)

    def assert_modified_date(self, expected_date, obj):
        expected_date = DateTime(expected_date)
        self.assertEquals(expected_date,
                          DateTime(obj.modified()),
                          'Wrong modification date on object.')
        self.assert_modified_date_in_catalog(expected_date, obj)

    def assert_modified_date_in_catalog(self, expected_date, obj):
        catalog = api.portal.get_tool('portal_catalog')
        catalog_uid = '/'.join(obj.getPhysicalPath())
        metadata = catalog.getMetadataForUID(catalog_uid)
        self.assertEquals(expected_date, metadata['modified'],
                          'Wrong modification date in catalog metadata.')

        # from date index
        t_tup = expected_date.toZone('UTC').parts()
        yr = t_tup[0]
        mo = t_tup[1]
        dy = t_tup[2]
        hr = t_tup[3]
        mn = t_tup[4]
        expected_val = ( ( ( ( yr * 12 + mo ) * 31 + dy ) * 24 + hr ) * 60 + mn )

        indexdata = catalog.getIndexDataForUID(catalog_uid)
        self.assertEquals(expected_val, indexdata['modified'],
                          'Wrong modification date in catalog index.')
