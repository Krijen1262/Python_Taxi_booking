# app/services/user_service.py

from typing import Optional, Dict, Any
import hashlib

from dataacesslayer.db_connector import Database
from dataacesslayer.user_dal import UserDAL
from dataacesslayer.customer_dal import CustomerDAL
from dataacesslayer.driver_dal import DriverDAL


class UserService:
    """
    Handles registration and login logic for users.
    Uses DAL classes to talk to the database.
    """

    def __init__(self, db: Database):
        self.db = db
        self.user_dal = UserDAL(db)
        self.customer_dal = CustomerDAL(db)
        self.driver_dal = DriverDAL(db)

    # -------------- internal helper ----------------

    def _hash_password(self, plain_password: str) -> str:
        """
        Simple SHA-256 hashing for passwords.
        (For assignment this is fine. In real apps use stronger hashing like bcrypt.)
        """
        return hashlib.sha256(plain_password.encode("utf-8")).hexdigest()

    # -------------- registration ----------------

    def register_customer(
        self,
        full_name: str,
        address: str,
        phone: str,
        email: str,
        username: str,
        password: str,
    ) -> int:
        """
        Register a new customer.
        - Creates a row in 'customers'
        - Creates a row in 'users' linked to that customer
        Returns the new user ID.
        """

        # Check if email already exists as a customer
        existing_customer = self.customer_dal.get_by_email(email)
        if existing_customer:
            raise ValueError("A customer with this email already exists.")

        # Check if username already exists
        existing_user = self.user_dal.get_by_username(username)
        if existing_user:
            raise ValueError("Username is already taken.")

        # 1) create customer
        customer_id = self.customer_dal.create_customer(
            full_name=full_name,
            address=address,
            phone=phone,
            email=email,
        )

        # 2) hash password and create user with role 'customer'
        password_hash = self._hash_password(password)

        user_id = self.user_dal.create_user(
            username=username,
            password_hash=password_hash,
            role="customer",
            customer_id=customer_id,
            driver_id=None,
        )

        return user_id

    def register_driver(
        self,
        full_name: str,
        address: str,
        phone: str,
        email: str,
        username: str,
        password: str,
        license_number: str,
        vehicle_number: str,
    ) -> int:
        """
        Register a new driver.
        - Creates a row in 'drivers'
        - Creates a row in 'users' linked to that driver
        Returns the new user ID.
        """

        existing_driver = self.driver_dal.get_by_email(email)
        if existing_driver:
            raise ValueError("A driver with this email already exists.")

        existing_user = self.user_dal.get_by_username(username)
        if existing_user:
            raise ValueError("Username is already taken.")

        # 1) create driver
        driver_id = self.driver_dal.create_driver(
            full_name=full_name,
            address=address,
            phone=phone,
            email=email,
            license_number=license_number,
            vehicle_number=vehicle_number,
            status="available",
        )

        # 2) create user with role 'driver'
        password_hash = self._hash_password(password)

        user_id = self.user_dal.create_user(
            username=username,
            password_hash=password_hash,
            role="driver",
            customer_id=None,
            driver_id=driver_id,
        )

        return user_id

    # -------------- login ----------------

    def login(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Validate user credentials.
        Returns the user row (dict) if login ok, otherwise None.
        """

        user = self.user_dal.get_by_username(username)
        if not user:
            return None

        if not user.get("is_active", 1):
            # user exists but is deactivated
            return None

        input_hash = self._hash_password(password)
        if input_hash != user["password_hash"]:
            return None

        # Login success
        return user
