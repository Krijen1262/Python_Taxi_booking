# app/dataaccesslayer/customer_dal.py

from typing import Optional, List, Dict, Any
from .base_dal import BaseDAL


class CustomerDAL(BaseDAL):
    """
    Data Access Layer for 'customers' table.
    """

    def create_customer(
        self,
        full_name: str,
        address: str,
        phone: str,
        email: str,
    ) -> int:
        """
        Insert a new customer and return the inserted ID.
        """
        query = """
            INSERT INTO customers (full_name, address, phone, email)
            VALUES (%s, %s, %s, %s)
        """
        params = (full_name, address, phone, email)

        cursor = self._get_cursor()
        cursor.execute(query, params)
        self.db.get_connection().commit()
        customer_id = cursor.lastrowid
        cursor.close()
        return customer_id

    def get_by_id(self, customer_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a customer by ID.
        """
        query = "SELECT * FROM customers WHERE id = %s"
        cursor = self._get_cursor()
        cursor.execute(query, (customer_id,))
        row = cursor.fetchone()
        cursor.close()
        return row

    def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Get a customer by email.
        """
        query = "SELECT * FROM customers WHERE email = %s"
        cursor = self._get_cursor()
        cursor.execute(query, (email,))
        row = cursor.fetchone()
        cursor.close()
        return row

    def list_all(self) -> List[Dict[str, Any]]:
        """
        Get all customers.
        """
        query = "SELECT * FROM customers"
        cursor = self._get_cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def update_customer(
        self,
        customer_id: int,
        full_name: str,
        address: str,
        phone: str,
        email: str,
    ) -> None:
        """
        Update a customer's details.
        """
        query = """
            UPDATE customers
            SET full_name = %s, address = %s, phone = %s, email = %s
            WHERE id = %s
        """
        params = (full_name, address, phone, email, customer_id)

        cursor = self._get_cursor()
        cursor.execute(query, params)
        self.db.get_connection().commit()
        cursor.close()

    def delete_customer(self, customer_id: int) -> None:
        """
        Delete a customer. Bookings will cascade if FK has ON DELETE CASCADE.
        """
        query = "DELETE FROM customers WHERE id = %s"
        cursor = self._get_cursor()
        cursor.execute(query, (customer_id,))
        self.db.get_connection().commit()
        cursor.close()
