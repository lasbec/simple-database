from collections.abc import MutableMapping
from ZODB import FileStorage, DB
import transaction
import os



class DataBase(MutableMapping):
    """An Object representing a database."""

    def __init__(self, full_path, auto_open=True):
        """"""  # todo writing proper docstrings
        self._full_path = full_path + '.fs'
        self._storage = None
        self._db = None
        self._connection = None
        self._root = None
        if auto_open:
            self.open()

    @property
    def full_path(self):
        return self._full_path[:-3]

    @property
    def name(self):
        return self.full_path.split('\\')[-1]

    @property
    def path(self):
        return '\\'.join(self.full_path.split('\\')[:-1])

    @property
    def is_opened(self):
        """"""  # todo docstings schreiben
        assert ((self._db is not None
                 and self._root is not None
                 and self._connection is not None
                 and self._storage is not None)
                !=
                (self._db is None
                 and self._root is None
                 and self._connection is None
                 and self._storage is None)
                )
        return self._db is not None

    @property
    def is_closed(self):
        """"""  # todo docstings schreiben
        return not self.is_opened

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __delitem__(self, key):
        """"""  # todo docstrings
        del self._root[key]

    def __getitem__(self, item):
        """"""  # todo docstrings
        return self._root[item]

    def __iter__(self):
        """"""  # todo docstrings
        return self._root.__iter__()

    def __len__(self):
        """"""  # todo docstrings
        return len(self._root)

    def __setitem__(self, key, value):
        """"""  # todo docstrings
        self._root[key] = value

    def _total_extinction(self):
        """"""  # todo docstrings
        self.close()
        os.remove(self._full_path)
        os.remove(self._full_path + '.index')
        os.remove(self._full_path + '.lock')
        os.remove(self._full_path + '.tmp')

    def keys(self):
        """"""  # todo docstrings
        return self._root.keys()

    def values(self):
        """"""  # todo docstrings
        return self._root.values()

    def open(self):
        """"""  # todo docstrings
        if self.is_opened:
            return 1
        else:
            self._storage = FileStorage.FileStorage(self._full_path)
            self._db = DB(self._storage)
            self._connection = self._db.open()
            self._root = self._connection.root()
            return 0

    def close(self):
        """"""  # todo docstrings
        if self.is_closed:
            return 1
        else:
            transaction.commit()
            self._connection.close()
            self._db.close()
            self._storage.close()
            self._storage = None
            self._db = None
            self._connection = None
            self._root = None
            return 0





class NotExistingDataBaseException(Exception):
    """"""  # todo docstrings
    # todo wie mache ich eine richtige Exception
    def __init__(self):
        """"""  # todo docstrings
        pass
