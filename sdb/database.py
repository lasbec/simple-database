from collections.abc import MutableMapping


class DataBase(MutableMapping):
    pass


class NotExistingDataBaseException(Exception):
    # todo wie mache ich eine richtige Exception
    def __init__(self):
        pass
