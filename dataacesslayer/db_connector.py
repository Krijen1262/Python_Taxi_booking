# app/dataaccesslayer/db_connector.py

import mysql.connector
from mysql.connector import Error
from config.settings import DB_CONFIG


class Database:
    """
    Handles MySQL connection and database/schema initialization.
    """

    def __init__(self):
        self.host = DB_CONFIG["host"]
        self.user = DB_CONFIG["user"]
        self.password = DB_CONFIG["password"]
        self.database_name = DB_CONFIG["database"]
        self.connection = None

        # Ensure DB exists, then connect to it
        self._ensure_database()
        self._connect_to_database()

    def _get_server_connection(self):
        """
        Connect to MySQL server WITHOUT specifying a database.
        Used for creating the database if it doesn't exist.
        """
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            return conn
        except Error as e:
            print(f"Error connecting to MySQL server: {e}")
            raise

    def _ensure_database(self):
        """
        Create the database if it does not exist.
        """
        try:
            conn = self._get_server_connection()
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database_name}")
            conn.commit()
            cursor.close()
            conn.close()
            print(f"Database '{self.database_name}' is ready.")
        except Error as e:
            print(f"Error ensuring database exists: {e}")
            raise

    def _connect_to_database(self):
        """
        Connect directly to the specific database.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database_name
            )
            if self.connection.is_connected():
                print(f"Connected to database '{self.database_name}'.")
        except Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def get_connection(self):
        """
        Public method to get the active connection.
        """
        if not self.connection or not self.connection.is_connected():
            self._connect_to_database()
        return self.connection

    def init_schema(self):
        """
        Create all necessary tables if they do not exist.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        # 1. customers table (full customer details)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS customers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(100) NOT NULL,
                address VARCHAR(255),
                phone VARCHAR(20),
                email VARCHAR(100) UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
                    ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB;
            """
        )

        # 2. drivers table (full driver details)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS drivers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(100) NOT NULL,
                address VARCHAR(255),
                phone VARCHAR(20),
                email VARCHAR(100) UNIQUE,
                license_number VARCHAR(50),
                vehicle_number VARCHAR(50),
                status ENUM('available', 'busy', 'inactive') DEFAULT 'available',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
                    ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB;
            """
        )

        # 3. users table (auth + role; references customers/drivers)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                role ENUM('customer', 'driver', 'admin') NOT NULL,
                customer_id INT NULL,
                driver_id INT NULL,
                is_active TINYINT(1) DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
                    ON UPDATE CURRENT_TIMESTAMP,
                CONSTRAINT fk_users_customer
                    FOREIGN KEY (customer_id) REFERENCES customers(id)
                    ON DELETE SET NULL,
                CONSTRAINT fk_users_driver
                    FOREIGN KEY (driver_id) REFERENCES drivers(id)
                    ON DELETE SET NULL
            ) ENGINE=InnoDB;
            """
        )

        # 4. bookings table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS bookings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT NOT NULL,
                pickup_location VARCHAR(255) NOT NULL,
                dropoff_location VARCHAR(255) NOT NULL,
                pickup_datetime DATETIME NOT NULL,
                status ENUM('pending', 'assigned', 'ongoing', 'completed', 'cancelled')
                    DEFAULT 'pending',
                driver_id INT NULL,
                fare DECIMAL(10, 2) NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
                    ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
                    ON DELETE CASCADE,
                FOREIGN KEY (driver_id) REFERENCES drivers(id)
                    ON DELETE SET NULL,
                INDEX idx_booking_driver_datetime (driver_id, pickup_datetime)
            ) ENGINE=InnoDB;
            """
        )

        conn.commit()
        cursor.close()
        print("Database schema initialised successfully.")

