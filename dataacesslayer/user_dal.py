# app/dataaccesslayer/user_dal.py

from typing import Optional, List, Dict, Any
from .base_dal import BaseDAL


class UserDAL(BaseDAL):
    """
    Data Access Layer for 'users' table.
    """

    def create_user(
        self,
        username: str,
        password_hash: str,  # if your column name is 'password', change here + SQL
        role: str,
        customer_id: Optional[int] = None,
        driver_id: Optional[int] = None,
    ) -> int:
        """
        Insert a new user and return the inserted user's ID.
        """
        query = """
            INSERT INTO users (username, password_hash, role, customer_id, driver_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (username, password_hash, role, customer_id, driver_id)

        cursor = self._get_cursor()
        cursor.execute(query, params)
        self.db.get_connection().commit()
        user_id = cursor.lastrowid
        cursor.close()
        return user_id

    def get_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a user by ID.
        """
        query = "SELECT * FROM users WHERE id = %s"
        cursor = self._get_cursor()
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
        cursor.close()
        return row

    def get_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Get a user by username.
        """
        query = "SELECT * FROM users WHERE username = %s"
        cursor = self._get_cursor()
        cursor.execute(query, (username,))
        row = cursor.fetchone()
        cursor.close()
        return row

    def list_all(self) -> List[Dict[str, Any]]:
        """
        Return all users.
        """
        query = "SELECT * FROM users"
        cursor = self._get_cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def deactivate_user(self, user_id: int) -> None:
        """
        Soft-delete (deactivate) a user.
        """
        query = "UPDATE users SET is_active = 0 WHERE id = %s"
        cursor = self._get_cursor()
        cursor.execute(query, (user_id,))
        self.db.get_connection().commit()
        cursor.close()

    def update_password(self, user_id: int, new_password_hash: str) -> None:
        """
        Update password hash for a user.
        """
        query = "UPDATE users SET password_hash = %s WHERE id = %s"
        cursor = self._get_cursor()
        cursor.execute(query, (new_password_hash, user_id))
        self.db.get_connection().commit()
        cursor.close()
