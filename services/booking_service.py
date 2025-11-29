# app/services/booking_service.py

from typing import Optional, List, Dict, Any
from datetime import datetime

from dataacesslayer.db_connector import Database
from dataacesslayer.booking_dal import BookingDAL
from dataacesslayer.driver_dal import DriverDAL


class BookingService:
    """
    Handles booking-related business logic:
    - customers: create/update/cancel/view bookings
    - admin: view all bookings, assign drivers (with overlap check)
    """

    def __init__(self, db: Database):
        self.db = db
        self.booking_dal = BookingDAL(db)
        self.driver_dal = DriverDAL(db)

    # ----------------- internal helpers -----------------

    def _parse_datetime(self, dt_str: str) -> datetime:
        """
        Parse a datetime string from user input.
        Expect format 'YYYY-MM-DD HH:MM', e.g. '2025-12-01 14:30'.
        Adjust format if you want a different one.
        """
        try:
            return datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("Invalid datetime format. Use 'YYYY-MM-DD HH:MM'.")

    # ----------------- customer-facing methods -----------------

    def create_booking_for_customer(
        self,
        customer_id: int,
        pickup_location: str,
        dropoff_location: str,
        pickup_datetime_str: str,
        notes: Optional[str] = None,
    ) -> int:
        """
        Customer books a taxi.
        Initially status is 'pending' and no driver is assigned.
        """
        pickup_dt = self._parse_datetime(pickup_datetime_str)

        booking_id = self.booking_dal.create_booking(
            customer_id=customer_id,
            pickup_location=pickup_location,
            dropoff_location=dropoff_location,
            pickup_datetime=pickup_dt,
            notes=notes,
        )
        return booking_id

    def get_customer_bookings(self, customer_id: int) -> List[Dict[str, Any]]:
        """
        Return all bookings for a given customer.
        """
        return self.booking_dal.list_by_customer(customer_id)

    def cancel_booking(self, booking_id: int, customer_id: int) -> None:
        """
        Customer cancels their own booking.
        Only allow cancel if the booking belongs to them
        and status is not 'completed' or already 'cancelled'.
        """
        booking = self.booking_dal.get_by_id(booking_id)
        if not booking:
            raise ValueError("Booking not found.")

        if booking["customer_id"] != customer_id:
            raise PermissionError("You can only cancel your own bookings.")

        if booking["status"] in ("completed", "cancelled"):
            raise ValueError(f"Cannot cancel a booking with status '{booking['status']}'.")

        self.booking_dal.cancel_booking(booking_id)

    def update_booking(
        self,
        booking_id: int,
        customer_id: int,
        pickup_location: str,
        dropoff_location: str,
        pickup_datetime_str: str,
        notes: Optional[str] = None,
    ) -> None:
        """
        Customer updates a booking.
        For simplicity, only allow update if booking is still 'pending'
        and belongs to that customer.
        """
        booking = self.booking_dal.get_by_id(booking_id)
        if not booking:
            raise ValueError("Booking not found.")

        if booking["customer_id"] != customer_id:
            raise PermissionError("You can only update your own bookings.")

        if booking["status"] != "pending":
            raise ValueError("Only 'pending' bookings can be updated.")

        pickup_dt = self._parse_datetime(pickup_datetime_str)

        self.booking_dal.update_booking(
            booking_id=booking_id,
            pickup_location=pickup_location,
            dropoff_location=dropoff_location,
            pickup_datetime=pickup_dt,
            notes=notes,
        )

    # ----------------- admin / driver methods -----------------

    def get_all_bookings(self) -> List[Dict[str, Any]]:
        """
        For admin: list all bookings.
        """
        return self.booking_dal.list_all()

    def get_bookings_for_driver(self, driver_id: int) -> List[Dict[str, Any]]:
        """
        For drivers: list all bookings assigned to a driver.
        """
        return self.booking_dal.list_by_driver(driver_id)

    def assign_driver_to_booking(
        self,
        booking_id: int,
        driver_id: int,
    ) -> None:
        """
        Admin assigns a driver to a booking.
        Ensures:
        - booking exists and is not cancelled/completed
        - driver exists
        - no overlapping booking for that driver at same pickup time
        """
        booking = self.booking_dal.get_by_id(booking_id)
        if not booking:
            raise ValueError("Booking not found.")

        if booking["status"] in ("cancelled", "completed"):
            raise ValueError(f"Cannot assign driver to a booking with status '{booking['status']}'.")

        driver = self.driver_dal.get_by_id(driver_id)
        if not driver:
            raise ValueError("Driver not found.")

        pickup_dt = booking["pickup_datetime"]

        # Check overlap for this driver
        has_overlap = self.booking_dal.has_overlapping_booking(
            driver_id=driver_id,
            pickup_datetime=pickup_dt,
        )
        if has_overlap:
            raise ValueError("This driver already has a booking at that time.")

        # If no overlap, assign driver
        self.booking_dal.assign_driver(booking_id, driver_id)
