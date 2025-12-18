from typing import Optional, Dict, Any
import hashlib

from dataacesslayer.db_connector import Database
from dataacesslayer.user_dal import UserDAL
from dataacesslayer.customer_dal import CustomerDAL
from dataacesslayer.driver_dal import DriverDAL


class UserService:
    """
    Uses DAL classes to communicate to the database.
    """

    def __init__(self, db: Database):
        self.db = db
        self.user_dal = UserDAL(db)
        self.customer_dal = CustomerDAL(db)
        self.driver_dal = DriverDAL(db)

    def _hash_password(self, plain_password: str) -> str:
        return hashlib.sha256(plain_password.encode("utf-8")).hexdigest()

    def register_customer(
        self,
        full_name: str,
        address: str,
        phone: str,
        email: str,
        username: str,
        password: str,
    ) -> int:
        existing_customer = self.customer_dal.get_by_email(email)
        if existing_customer:
            raise ValueError("A customer with this email already exists.")

        existing_user = self.user_dal.get_by_username(username)
        if existing_user:
            raise ValueError("Username is already taken.")

        customer_id = self.customer_dal.create_customer(
            full_name=full_name,
            address=address,
            phone=phone,
            email=email,
        )

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
        """
        existing_driver = self.driver_dal.get_by_email(email)
        if existing_driver:
            raise ValueError("A driver with this email already exists.")

        existing_user = self.user_dal.get_by_username(username)
        if existing_user:
            raise ValueError("Username is already taken.")

        driver_id = self.driver_dal.create_driver(
            full_name=full_name,
            address=address,
            phone=phone,
            email=email,
            license_number=license_number,
            vehicle_number=vehicle_number,
            status="available",
        )

        password_hash = self._hash_password(password)

        user_id = self.user_dal.create_user(
            username=username,
            password_hash=password_hash,
            role="driver",
            customer_id=None,
            driver_id=driver_id,
        )

        return user_id

    def login(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Validate user credentials.
        """
        user = self.user_dal.get_by_username(username)
        if not user:
            return None

        if not user.get("is_active", 1):
            return None

        input_hash = self._hash_password(password)
        if input_hash != user["password_hash"]:
            return None

        role = user.get("role")
        
        if role == "customer" and user.get("customer_id"):
            customer = self.customer_dal.get_by_id(user["customer_id"])
            if customer:
                original_user_id = user.get("id")
                user.update(customer)
                user["id"] = user["customer_id"]
                user["user_id"] = original_user_id
        elif role == "driver" and user.get("driver_id"):
            driver = self.driver_dal.get_by_id(user["driver_id"])
            if driver:
                original_user_id = user.get("id")
                user.update(driver)
                user["id"] = user["driver_id"]
                user["user_id"] = original_user_id

        return user
