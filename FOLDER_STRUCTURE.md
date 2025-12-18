# Python Taxi Booking - Folder Structure

```
Python_Taxi_booking/
│
├── config/
│   ├── __pycache__/
│   └── settings.py
│
├── dataacesslayer/
│   ├── __pycache__/
│   ├── base_dal.py
│   ├── booking_dal.py
│   ├── customer_dal.py
│   ├── db_connector.py
│   ├── driver_dal.py
│   └── user_dal.py
│
├── services/
│   ├── __pycache__/
│   ├── booking_service.py
│   ├── customer_service.py
│   ├── driver_service.py
│   └── user_services.py
│
├── ui/
│   ├── __pycache__/
│   ├── admin_dashboard.py
│   ├── app_context.py
│   ├── customer_dashboard.py
│   ├── driver_dashboard.py
│   ├── login_page.py
│   ├── main_app.py
│   └── register_page.py
│
├── 2432413_KRIJEN_SHAHI_MCCT.pdf
├── main.py
├── README.md
└── run_gui.py
```

## Directory Descriptions

### `/config`
Configuration files and settings
- `settings.py` - Application configuration settings

### `/dataacesslayer`
Data Access Layer - Database interaction modules
- `base_dal.py` - Base data access layer class
- `booking_dal.py` - Booking data access operations
- `customer_dal.py` - Customer data access operations
- `db_connector.py` - Database connection handler
- `driver_dal.py` - Driver data access operations
- `user_dal.py` - User data access operations

### `/services`
Business logic layer - Service modules
- `booking_service.py` - Booking business logic
- `customer_service.py` - Customer business logic
- `driver_service.py` - Driver business logic
- `user_services.py` - User business logic

### `/ui`
User Interface layer - GUI components
- `admin_dashboard.py` - Admin dashboard interface
- `app_context.py` - Application context management
- `customer_dashboard.py` - Customer dashboard interface
- `driver_dashboard.py` - Driver dashboard interface
- `login_page.py` - Login page interface
- `main_app.py` - Main application window
- `register_page.py` - Registration page interface

### Root Files
- `main.py` - Main entry point
- `run_gui.py` - GUI application launcher
- `README.md` - Project documentation
- `2432413_KRIJEN_SHAHI_MCCT.pdf` - Project documentation PDF

