from typing import Optional, List, Dict, Any
from datetime import datetime
from .base_dal import BaseDAL


class BookingDAL(BaseDAL):
    """
    Data Access Layer for 'bookings' table.
    """

    def create_booking(
        self,
        customer_id: int,
        pickup_location: str,
        dropoff_location: str,
        pickup_datetime: datetime,
        notes: Optional[str] = None,
    ) -> int:
        """
        Insert a new booking with status 'pending'.
        """
        query = """
            INSERT INTO bookings (
                customer_id,
                pickup_location,
                dropoff_location,
                pickup_datetime,
                status,
                notes
            )
            VALUES (%s, %s, %s, %s, 'pending', %s)
        """
        params = (
            customer_id,
            pickup_location,
            dropoff_location,
            pickup_datetime,
            notes,
        )

        cursor = self._get_cursor()
        cursor.execute(query, params)
        self.db.get_connection().commit()
        booking_id = cursor.lastrowid
        cursor.close()
        return booking_id

    def get_by_id(self, booking_id: int) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM bookings WHERE id = %s"
        cursor = self._get_cursor()
        cursor.execute(query, (booking_id,))
        row = cursor.fetchone()
        cursor.close()
        return row

    def list_by_customer(self, customer_id: int) -> List[Dict[str, Any]]:
        query = """
            SELECT
                id,
                customer_id,
                driver_id,
                pickup_location,
                dropoff_location,
                pickup_datetime,
                DATE(pickup_datetime) AS pickup_date,
                TIME(pickup_datetime) AS pickup_time,
                status,
                notes
            FROM bookings
            WHERE customer_id = %s
            ORDER BY pickup_datetime DESC
        """
        cursor = self._get_cursor()
        cursor.execute(query, (customer_id,))
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def list_by_driver(self, driver_id: int) -> List[Dict[str, Any]]:
        query = """
            SELECT
                id,
                customer_id,
                driver_id,
                pickup_location,
                dropoff_location,
                pickup_datetime,
                DATE(pickup_datetime) AS pickup_date,
                TIME(pickup_datetime) AS pickup_time,
                status,
                notes
            FROM bookings
            WHERE driver_id = %s
            ORDER BY pickup_datetime DESC
        """
        cursor = self._get_cursor()
        cursor.execute(query, (driver_id,))
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def list_all(self) -> List[Dict[str, Any]]:
        query = """
            SELECT
                id,
                customer_id,
                driver_id,
                pickup_location,
                dropoff_location,
                pickup_datetime,
                DATE(pickup_datetime) AS pickup_date,
                TIME(pickup_datetime) AS pickup_time,
                status,
                notes
            FROM bookings
            ORDER BY pickup_datetime DESC
        """
        cursor = self._get_cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def cancel_booking(self, booking_id: int) -> None:
        """
        Mark a booking as 'cancelled'.
        """
        query = "UPDATE bookings SET status = 'cancelled' WHERE id = %s"
        cursor = self._get_cursor()
        cursor.execute(query, (booking_id,))
        self.db.get_connection().commit()
        cursor.close()

    def update_booking(
        self,
        booking_id: int,
        pickup_location: str,
        dropoff_location: str,
        pickup_datetime: datetime,
        notes: Optional[str] = None,
    ) -> None:
        """
        Update basic booking details.
        """
        query = """
            UPDATE bookings
            SET pickup_location = %s,
                dropoff_location = %s,
                pickup_datetime = %s,
                notes = %s
            WHERE id = %s
        """
        params = (
            pickup_location,
            dropoff_location,
            pickup_datetime,
            notes,
            booking_id,
        )

        cursor = self._get_cursor()
        cursor.execute(query, params)
        self.db.get_connection().commit()
        cursor.close()

    def assign_driver(self, booking_id: int, driver_id: int) -> None:
        """
        Assign a driver and change status to 'assigned'.
        """
        query = """
            UPDATE bookings
            SET driver_id = %s, status = 'assigned'
            WHERE id = %s
        """
        cursor = self._get_cursor()
        cursor.execute(query, (driver_id, booking_id))
        self.db.get_connection().commit()
        cursor.close()

    def update_status(self, booking_id: int, status: str) -> None:
        """
        Update the status of a booking.
        """
        query = "UPDATE bookings SET status = %s WHERE id = %s"
        cursor = self._get_cursor()
        cursor.execute(query, (status, booking_id))
        self.db.get_connection().commit()
        cursor.close()

    def has_active_booking_for_driver(self, driver_id: int) -> bool:
        """
        Check if the driver already has any active booking
        (pending/assigned/ongoing). Used to prevent overlapping rides.
        """
        query = """
            SELECT COUNT(*) AS cnt
            FROM bookings
            WHERE driver_id = %s
              AND status IN ('pending', 'assigned', 'ongoing')
        """
        cursor = self._get_cursor()
        cursor.execute(query, (driver_id,))
        row = cursor.fetchone()
        cursor.close()
        return row["cnt"] > 0 if row else False
