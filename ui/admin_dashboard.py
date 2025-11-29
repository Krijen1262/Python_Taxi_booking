# app/ui/admin_dashboard.py

import tkinter as tk
from tkinter import messagebox


class AdminDashboard(tk.Frame):
    """
    Basic admin dashboard.
    Later we will:
    - display list of all bookings
    - allow assigning drivers using BookingService.assign_driver_to_booking
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.user = None

        self.header_label = tk.Label(self, text="Admin Dashboard", font=("Arial", 20, "bold"))
        self.header_label.pack(pady=20)

        self.info_label = tk.Label(self, text="", font=("Arial", 12))
        self.info_label.pack(pady=10)

        tk.Button(self, text="View All Bookings (TODO)", width=25,
                  command=self.view_bookings_placeholder).pack(pady=5)

        tk.Button(self, text="Assign Driver (TODO)", width=25,
                  command=self.assign_driver_placeholder).pack(pady=5)

        tk.Button(self, text="Logout", width=15,
                  command=self.controller.logout).pack(pady=20)

    def set_user(self, user: dict):
        self.user = user
        self.info_label.config(
            text=f"Logged in as: {user['username']} (Admin)"
        )

    def view_bookings_placeholder(self):
        messagebox.showinfo("Info", "View all bookings UI will be implemented here.")

    def assign_driver_placeholder(self):
        messagebox.showinfo("Info", "Assign driver UI will be implemented here.")
