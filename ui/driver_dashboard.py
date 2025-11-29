# app/ui/driver_dashboard.py

import tkinter as tk
from tkinter import messagebox


class DriverDashboard(tk.Frame):
    """
    Basic driver dashboard.
    Later we will:
    - call BookingService.get_bookings_for_driver
    - show assigned trips in a list
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.user = None

        self.header_label = tk.Label(self, text="Driver Dashboard", font=("Arial", 20, "bold"))
        self.header_label.pack(pady=20)

        self.info_label = tk.Label(self, text="", font=("Arial", 12))
        self.info_label.pack(pady=10)

        tk.Button(self, text="View My Trips (TODO)", width=25,
                  command=self.view_trips_placeholder).pack(pady=5)

        tk.Button(self, text="Logout", width=15,
                  command=self.controller.logout).pack(pady=20)

    def set_user(self, user: dict):
        self.user = user
        self.info_label.config(
            text=f"Logged in as: {user['username']} (Driver ID: {user.get('driver_id')})"
        )

    def view_trips_placeholder(self):
        messagebox.showinfo("Info", "View trips UI will be implemented here.")
