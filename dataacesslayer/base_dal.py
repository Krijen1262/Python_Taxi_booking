from .db_connector import Database


class BaseDAL:
    """
    Base Data Access Layer class to be inherited by all DALs.
    Holds the shared Database instance and provides a helper for cursors.
    """

    def __init__(self, db: Database):
        self.db = db

    def _get_cursor(self, dictionary: bool = True):
        conn = self.db.get_connection()
        return conn.cursor(dictionary=dictionary)
