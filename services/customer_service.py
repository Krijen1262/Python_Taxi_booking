from typing import List, Dict, Any, Optional

from dataacesslayer.db_connector import Database
from dataacesslayer.customer_dal import CustomerDAL


class CustomerService:

    def __init__(self, db: Database):
        self.db = db
        self.customer_dal = CustomerDAL(db)

    def list_all(self) -> List[Dict[str, Any]]:
        """Return all customers."""
        return self.customer_dal.list_all()

    def get_by_id(self, customer_id: int) -> Optional[Dict[str, Any]]:
        """Get a single customer by ID."""
        return self.customer_dal.get_by_id(customer_id)


