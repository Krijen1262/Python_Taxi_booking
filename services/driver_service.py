from typing import List, Dict, Any, Optional

from dataacesslayer.db_connector import Database
from dataacesslayer.driver_dal import DriverDAL


class DriverService:


    def __init__(self, db: Database):
        self.db = db
        self.driver_dal = DriverDAL(db)

    def list_all(self) -> List[Dict[str, Any]]:
        """Return all drivers."""
        return self.driver_dal.list_all()

    def list_available(self) -> List[Dict[str, Any]]:
        """Return drivers whose status is 'available'."""
        return self.driver_dal.list_available()

    def get_by_id(self, driver_id: int) -> Optional[Dict[str, Any]]:
        """Get a single driver by ID."""
        return self.driver_dal.get_by_id(driver_id)

    def update_status(self, driver_id: int, status: str) -> None:
        """Update driver status ('available', 'busy', 'inactive')."""
        self.driver_dal.update_status(driver_id, status)


