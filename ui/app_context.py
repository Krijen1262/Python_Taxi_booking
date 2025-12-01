from dataacesslayer.db_connector import Database
from services.user_services import UserService
from services.booking_service import BookingService
from services.driver_service import DriverService
from services.customer_service import CustomerService


class AppContext:
    """
    Holds shared objects for the whole application:
    - Database
    - Services (UserService, BookingService, etc.)
    """

    def __init__(self):
        self.db = Database()
        self.db.init_schema()

        self.user_service = UserService(self.db)
        self.booking_service = BookingService(self.db)
        # Services used by admin / driver dashboards
        self.driver_service = DriverService(self.db)
        self.customer_service = CustomerService(self.db)
