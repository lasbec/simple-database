import unittest
from unittest import TestCase
import os
from database import DataBase, NotExistingDataBaseException


class DataBaseTest0(TestCase):
    db_path = 'tests'
    db_name = 'general_test_base'

    def __init__(self, *args, **kwargs):
        TestCase.__init__(self, *args, **kwargs)
        self.immutables = [True, False,
                           None,
                           7357, 42,
                           (True, 69), (1337, ()),
                           '\n +  \t', 'test',
                           frozenset([1, "a", "\n"]), frozenset([1, ('r', 2), "a", "\n"])]
        self.db_path = 'tests'
        self.db_name = 'general_test_base'
        self.full_db_path = self.db_path + '\\' + self.db_name

    def setUp(self):
        self.db = DataBase(self.full_db_path)

    def tearDown(self):
        self.db._total_extinction()

    def assert_db_is_proper_closed(self, db):
        self.assertIsNone(db._db)
        self.assertIsNone(db._root)
        self.assertIsNone(db._storage)
        self.assertIsNone(db._connection)
        self.assertTrue(db.is_closed)
        self.assertFalse(db.is_opened)

    def assert_db_is_proper_opened(self, db):
        self.assertIsNotNone(db._db)
        self.assertIsNotNone(db._root)
        self.assertIsNotNone(db._storage)
        self.assertIsNotNone(db._connection)
        self.assertFalse(db.is_closed)
        self.assertTrue(db.is_opened)

    def test_basics(self):
        """Tests creating, opening, closing and deleting a database."""
        # test the creation for a database
        db_path = 'tests'
        db_name = 'basic_tests'
        full_path = db_path + '\\' + db_name
        db = DataBase(full_path)

        self.assertEqual(db.name, db_name)
        self.assertEqual(db.path, db_path)
        self.assertEqual(db.full_path, full_path)
        self.assertTrue(os.path.exists(full_path + '.fs'))
        self.assertTrue(os.path.exists(full_path + '.fs.index'))
        self.assertTrue(os.path.exists(full_path + '.fs.lock'))
        self.assertTrue(os.path.exists(full_path + '.fs.tmp'))

        # test closing the DataBase object
        ret = db.close()
        self.assertEqual(ret, 0)
        self.assert_db_is_proper_closed(db)

        # test recloseing the DataBase object
        ret = db.close()
        self.assertEqual(ret, 1)
        self.assert_db_is_proper_closed(db)

        # test opening a DataBase object
        ret = db.open()
        self.assertEqual(ret, 0)
        self.assert_db_is_proper_opened(db)

        # test reopeing a DataBase object
        ret = db.open()
        self.assertEqual(ret, 1)
        self.assert_db_is_proper_opened(db)

        # test _total_extinction of the database
        db._total_extinction()

        self.assertFalse(os.path.exists(full_path + '.fs'))
        self.assertFalse(os.path.exists(full_path + '.fs.index'))
        self.assertFalse(os.path.exists(full_path + '.fs.lock'))
        self.assertFalse(os.path.exists(full_path + '.fs.tmp'))

        # test recreating database
        ret = db.open()
        self.assertEqual(ret, 0)
        self.assert_db_is_proper_opened(db)

        db._total_extinction()

    def test_context_manager(self):
        """"""  # todo docstrings schreiben
        db_path = 'tests'
        db_name = 'context_manager_test'
        full_path = db_path + '\\' + db_name
        immutables_rev = list(reversed(self.immutables))
        test_root = zip(immutables_rev, self.immutables)

        # writing data into database
        with DataBase(full_path) as db:
            self.assert_db_is_proper_opened(db)
            for key, value in test_root:
                db[key] = value

        # ensure that the database was closed by checking if accessing is possible
        db = DataBase(full_path)

        # checking correctness and completeness of stored data
        for key, value in test_root:
            self.assertIn(key, db.keys())
            self.assertIn(value, db.values())
            self.assertEqual(db[key], value)

        # manual teardown
        db._total_extinction()

    def test_auto_open(self):
        """Testing the constructor on the functionality of the parameter auto_open."""
        # todo implement

    def test_simple_immutable_storage(self):
        """Tests persistence of little amount of immutable objects when stored in a DataBase object."""
        immutables_rev = list(reversed(self.immutables))
        test_root = zip(immutables_rev, self.immutables)
        for key, value in test_root:
            self.db[key] = value

        self.db.close()
        self.db.open()

        for key, value in test_root:
            self.assertIn(key, self.db.keys())
            self.assertIn(value, self.db.values())
            self.assertEqual(self.db[key], value)


if __name__ == '__main__':
    unittest.main()
