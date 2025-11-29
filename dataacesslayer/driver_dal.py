# app/dataaccesslayer/driver_dal.py

from typing import Optional, List, Dict, Any
from .base_dal import BaseDAL


class DriverDAL(BaseDAL):
    """
    Data Access Layer for 'drivers' table.
    """

    def create_driver(
        self,
        full_name: str,
        address: str,
        phone: str,
        email: str,
        license_number: str,
        vehicle_number: str,
        status: str = "available",
    ) -> int:
        """
        Insert a new driver and return the inserted ID.
        """
        query = """
            INSERT INTO drivers (
                full_name, address, phone, email,
                license_number, vehicle_number, status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            full_name,
            address,
            phone,
            email,
            license_number,
            vehicle_number,
            status,
        )

        cursor = self._get_cursor()
        cursor.execute(query, params)
        self.db.get_connection().commit()
        driver_id = cursor.lastrowid
        cursor.close()
        return driver_id

    def get_by_id(self, driver_id: int) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM drivers WHERE id = %s"
        cursor = self._get_cursor()
        cursor.execute(query, (driver_id,))
        row = cursor.fetchone()
        cursor.close()
        return row

    def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM drivers WHERE email = %s"
        cursor = self._get_cursor()
        cursor.execute(query, (email,))
        row = cursor.fetchone()
        cursor.close()
        return row

    def list_all(self) -> List[Dict[str, Any]]:
        query = "SELECT * FROM drivers"
        cursor = self._get_cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def list_available(self) -> List[Dict[str, Any]]:
        """
        Get drivers whose status is 'available'.
        """
        query = "SELECT * FROM drivers WHERE status = 'available'"
        cursor = self._get_cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def update_status(self, driver_id: int, status: str) -> None:
        """
        Update driver status to 'available', 'busy', or 'inactive'.
        """
        query = "UPDATE drivers SET status = %s WHERE id = %s"
        cursor = self._get_cursor()
        cursor.execute(query, (status, driver_id))
        self.db.get_connection().commit()
        cursor.close()

    def update_driver(
        self,
        driver_id: int,
        full_name: str,
        address: str,
        phone: str,
        email: str,
        license_number: str,
        vehicle_number: str,
    ) -> None:
        query = """
            UPDATE drivers
            SET full_name = %s, address = %s, phone = %s, email = %s,
                license_number = %s, vehicle_number = %s
            WHERE id = %s
        """
        params = (
            full_name,
            address,
            phone,
            email,
            license_number,
            vehicle_number,
            driver_id,
        )

        cursor = self._get_cursor()
        cursor.execute(query, params)
        self.db.get_connection().commit()
        cursor.close()
