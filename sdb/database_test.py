import unittest
import os
from .database import DataBase, NotExistingDataBaseException


class DataBaseTest0(unittest.TestCase):
    db_path = 'tests'
    db_name = 'test_base'

    def assert_db_is_proper_closed(self, db):
        self.assertIsNone(db.db)
        self.assertIsNone(db.root)
        self.assertIsNone(db.storage)
        self.assertIsNone(db.connection)
        self.assertTrue(db.is_closed)
        self.assertFalse(db.is_opend)

    def assert_db_is_proper_opened(self, db):
        self.assertIsNotNone(db.db)
        self.assertIsNotNone(db.root)
        self.assertIsNotNone(db.storage)
        self.assertIsNotNone(db.connection)
        self.assertFalse(db.is_closed)
        self.assertTrue(db.is_opend)

    def test_basics(self):
        # test the creation for a database
        full_path = DataBaseTest0.db_path + '\\' + DataBaseTest0.db_name
        db = DataBase(full_path)

        self.assertEquals(db.name, DataBaseTest0.db_name)
        self.assertEquals(db.path, DataBaseTest0.db_path)
        self.assertEquals(db.full_path, full_path)
        self.assertTrue(os.path.exists(DataBaseTest0.db_path + '.fs'))
        self.assertTrue(os.path.exists(DataBaseTest0.db_path + '.fs.index'))
        self.assertTrue(os.path.exists(DataBaseTest0.db_path + '.fs.lock'))
        self.assertTrue(os.path.exists(DataBaseTest0.db_path + '.fs.tmp'))

        # test closing the DataBase object
        ret = db.close()
        self.assertEquals(ret, 0)
        self.assert_db_is_proper_closed(db)

        # test recloseing the DataBase object
        ret = db.close()
        self.assertAlmostEquals(ret, 1)
        self.assert_db_is_proper_closed(db)

        # test opening a DataBase object
        ret = db.opend()
        self.assertEquals(ret, 0)
        self.assert_db_is_proper_opened(db)

        # test reopeing a DataBase object
        ret = db.opend()
        self.assertEquals(ret, 1)
        self.assert_db_is_proper_opened(db)

        # test _total_extinction of the database
        db._total_extinction()

        self.assertFalse(os.path.exists(DataBaseTest0.db_path + '.fs'))
        self.assertFalse(os.path.exists(DataBaseTest0.db_path + '.fs.index'))
        self.assertFalse(os.path.exists(DataBaseTest0.db_path + '.fs.lock'))
        self.assertFalse(os.path.exists(DataBaseTest0.db_path + '.fs.tmp'))

        # test acessing an attribute from an extinctioned database
        for attr in dir(db):
            self.assertRaises(NotExistingDataBaseException, getattr, db, attr)
            warning = ' '  # todo waring regex
            self.assertWarnsRegex(warning, getattr, db, attr)

        # test deleting the object
        test_var = db
        del db
        try:
            test_var
            self.assertTrue(False)
        except NameError:
            self.assertTrue(True)
