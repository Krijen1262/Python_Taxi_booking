
import tkinter as tk
from typing import Dict

from ui.app_context import AppContext
from ui.login_page import LoginPage
from ui.register_page import RegisterPage
from ui.customer_dashboard import CustomerDashboard
from ui.driver_dashboard import DriverDashboard
from ui.admin_dashboard import AdminDashboard


class MainApp(tk.Tk):
    """
    Root Tkinter application.
    Manages switching between LoginPage, RegisterPage and dashboards
    in the same window/frame.
    """

    def __init__(self, context: AppContext):
        super().__init__()
        self.title("Taxi Booking System")
        self.geometry("900x600")

        self.context = context
        self.current_user = None

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames: Dict[str, tk.Frame] = {}

        for PageClass in (
            LoginPage,
            RegisterPage,
            CustomerDashboard,
            DriverDashboard,
            AdminDashboard,
        ):
            page_name = PageClass.__name__
            frame = PageClass(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name: str):
        """
        Bring a frame to the front.
        """
        frame = self.frames.get(page_name)
        if frame is None:
            raise ValueError(f"No frame named '{page_name}'")
        frame.tkraise()

    def set_current_user(self, user: dict):
        """
        Store the logged-in user dict.
        """
        self.current_user = user

    def logout(self):
        """
        Log out current user and go back to LoginPage.
        """
        self.current_user = None
        self.show_frame("LoginPage")
