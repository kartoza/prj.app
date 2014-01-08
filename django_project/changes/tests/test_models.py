from django.test import TestCase
from changes.tests.model_factories import CategoryF, EntryF, VersionF


class TestCategoryCRUD(TestCase):
    """
    Tests search models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_Category_create(self):
        """
        Tests Category model creation
        """
        myModel = CategoryF.create()

        #check if PK exists
        self.assertTrue(myModel.pk is not None)

        #check if name exists
        self.assertTrue(myModel.name is not None)

    def test_Category_read(self):
        """
        Tests Category model read
        """
        myModel = CategoryF.create(
            name=u'Custom Category'
        )

        self.assertTrue(myModel.name == 'Custom Category')
        self.assertTrue(myModel.slug == 'custom-category')

    def test_Category_update(self):
        """
        Tests Category model update
        """
        myModel = CategoryF.create()
        myNewModelData = {
            'name': u'New Category Name',
            'description': u'New description',
            'approved': False,
            'private': True,
        }
        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val)

    def test_Category_delete(self):
        """
        Tests Category model delete
        """
        myModel = CategoryF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)


class TestEntryCRUD(TestCase):
    """
    Tests search models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_Entry_create(self):
        """
        Tests Entry model creation
        """
        myModel = EntryF.create()

        #check if PK exists
        self.assertTrue(myModel.pk is not None)

        #check if name exists
        self.assertTrue(myModel.title is not None)

    def test_Entry_read(self):
        """
        Tests Entry model read
        """
        myModel = EntryF.create(
            title=u'Custom Entry'
        )

        self.assertTrue(myModel.title == 'Custom Entry')
        self.assertTrue(myModel.slug == 'custom-entry')

    def test_Entry_update(self):
        """
        Tests Entry model update
        """
        myModel = EntryF.create()
        myNewModelData = {
            'name': u'New Entry Name',
            'description': u'New description',
            'approved': False,
            'private': True,
        }
        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val)

    def test_Entry_delete(self):
        """
        Tests Entry model delete
        """
        myModel = EntryF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)


class TestVersionCRUD(TestCase):
    """
    Tests search models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_Version_create(self):
        """
        Tests Version model creation
        """
        myModel = VersionF.create()

        #check if PK exists
        self.assertTrue(myModel.pk is not None)

        #check if name exists
        self.assertTrue(myModel.name is not None)

    def test_Version_read(self):
        """
        Tests Version model read
        """
        myModel = VersionF.create(
            name=u'Custom Version'
        )

        self.assertTrue(myModel.name == 'Custom Version')
        self.assertTrue(myModel.slug == 'custom-version')

    def test_Version_update(self):
        """
        Tests Version model update
        """
        myModel = VersionF.create()
        myNewModelData = {
            'name': u'New Version Name',
            'description': u'New description',
            'approved': True
        }
        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val)

    def test_Version_delete(self):
        """
        Tests Version model delete
        """
        myModel = VersionF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)
