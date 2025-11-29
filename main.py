# main.py

from dataacesslayer.db_connector import Database
from dataacesslayer.customer_dal import CustomerDAL
from dataacesslayer.user_dal import UserDAL

if __name__ == "__main__":
    db = Database()
    db.init_schema()

    customer_dal = CustomerDAL(db)
    user_dal = UserDAL(db)

    cust_id = customer_dal.create_customer(
        full_name="Test Customer",
        address="Dhulikhel",
        phone="9800000000",
        email="test@example.com",
    )

    user_id = user_dal.create_user(
        username="testuser",
        password_hash="plainpassword_for_now",
        role="customer",
        customer_id=cust_id,
    )

    print("Created customer_id:", cust_id)
    print("Created user_id:", user_id)
