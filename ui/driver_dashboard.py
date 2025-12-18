# ui/driver_dashboard.py

import tkinter as tk
from tkinter import ttk, messagebox


class DriverDashboard(tk.Frame):
    """
    Driver Dashboard with menu access to:
    - View Assigned Trips
    - Update Status
    - View Profile
    """

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f8fafc")
        self.controller = controller
        self.user = None

        # Main container
        self.container = tk.Frame(self, bg="#f8fafc")
        self.container.pack(fill="both", expand=True)

    def set_user(self, user):
        """Set current user and build dashboard"""
        self.user = user
        self._build_dashboard()

    def _build_dashboard(self):
        """Build the dashboard UI"""
        # Clear existing widgets
        for widget in self.container.winfo_children():
            widget.destroy()

        header = tk.Frame(self.container, bg="#10b981", height=80)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        header_content = tk.Frame(header, bg="#10b981")
        header_content.pack(fill="both", expand=True, padx=30, pady=15)

        tk.Label(
            header_content,
            text=f"Driver Dashboard - {self.user.get('full_name', 'Driver')}",
            font=("Segoe UI", 20, "bold"),
            bg="#10b981",
            fg="white"
        ).pack(side="left")

        status = self.user.get('status', 'available')
        status_color = "#22c55e" if status == "available" else "#ef4444" if status == "busy" else "#6b7280"
        
        status_frame = tk.Frame(header_content, bg="#10b981")
        status_frame.pack(side="right", padx=(0, 20))
        
        tk.Label(
            status_frame,
            text=f"Status: {status.upper()}",
            font=("Segoe UI", 11, "bold"),
            bg=status_color,
            fg="white",
            padx=15,
            pady=5
        ).pack()

        logout_btn = tk.Button(
            header_content,
            text="Logout",
            font=("Segoe UI", 10),
            bg="#f87171",
            fg="white",
            activebackground="#dc2626",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self._logout,
            padx=20,
            pady=8
        )
        logout_btn.pack(side="right")

        main_content = tk.Frame(self.container, bg="#f8fafc")
        main_content.pack(fill="both", expand=True, padx=30, pady=20)

        sidebar = tk.Frame(main_content, bg="white", width=250)
        sidebar.pack(side="left", fill="y", padx=(0, 20))
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="Driver Menu",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#1f2937"
        ).pack(pady=20)

        menu_items = [
            ("🚗 My Trips", self._show_assigned_trips),
            ("📊 Update Status", self._show_status_update),
            ("👤 My Profile", self._show_profile),
        ]

        for text, command in menu_items:
            btn = tk.Button(
                sidebar,
                text=text,
                font=("Segoe UI", 11),
                bg="white",
                fg="#374151",
                activebackground="#d1fae5",
                activeforeground="#10b981",
                relief="flat",
                cursor="hand2",
                command=command,
                anchor="w",
                padx=20,
                pady=12
            )
            btn.pack(fill="x", padx=10, pady=2)

        self.content_area = tk.Frame(main_content, bg="white")
        self.content_area.pack(side="right", fill="both", expand=True)

        self._show_assigned_trips()

    def _show_assigned_trips(self):
        """Show driver's assigned trips"""
        for widget in self.content_area.winfo_children():
            widget.destroy()

        trips_frame = tk.Frame(self.content_area, bg="white")
        trips_frame.pack(fill="both", expand=True, padx=40, pady=30)

        tk.Label(
            trips_frame,
            text="My Assigned Trips",
            font=("Segoe UI", 18, "bold"),
            bg="white",
            fg="#1f2937"
        ).pack(anchor="w", pady=(0, 20))

        try:
            booking_service = self.controller.context.booking_service
            trips = booking_service.get_driver_bookings(self.user['id'])

            if not trips:
                tk.Label(
                    trips_frame,
                    text="No trips assigned yet",
                    font=("Segoe UI", 12),
                    bg="white",
                    fg="#6b7280"
                ).pack(pady=50)
                return

            canvas = tk.Canvas(trips_frame, bg="white", highlightthickness=0)
            scrollbar = ttk.Scrollbar(trips_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="white")

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            for trip in trips:
                card = tk.Frame(
                    scrollable_frame,
                    bg="#f9fafb",
                    relief="solid",
                    bd=1,
                    highlightbackground="#e5e7eb",
                    highlightthickness=1
                )
                card.pack(fill="x", pady=10, padx=5)

                card_inner = tk.Frame(card, bg="#f9fafb")
                card_inner.pack(fill="both", expand=True, padx=20, pady=15)

                header_row = tk.Frame(card_inner, bg="#f9fafb")
                header_row.pack(fill="x", pady=(0, 10))

                tk.Label(
                    header_row,
                    text=f"Trip #{trip['id']}",
                    font=("Segoe UI", 13, "bold"),
                    bg="#f9fafb",
                    fg="#1f2937"
                ).pack(side="left")

                status_color = {
                    "pending": "#f59e0b",
                    "confirmed": "#10b981",
                    "completed": "#6b7280",
                    "cancelled": "#ef4444"
                }.get(trip['status'], "#6b7280")

                tk.Label(
                    header_row,
                    text=trip['status'].upper(),
                    font=("Segoe UI", 9, "bold"),
                    bg=status_color,
                    fg="white",
                    padx=10,
                    pady=3
                ).pack(side="right")

                details = [
                    ("📍 Pickup:", trip['pickup_location']),
                    ("📍 Drop-off:", trip['dropoff_location']),
                    ("📅 Date:", trip['pickup_date']),
                    ("🕐 Time:", trip['pickup_time']),
                    ("👤 Customer:", trip.get('customer_name', 'N/A')),
                    ("📞 Phone:", trip.get('customer_phone', 'N/A')),
                ]

                for label, value in details:
                    row = tk.Frame(card_inner, bg="#f9fafb")
                    row.pack(fill="x", pady=3)

                    tk.Label(
                        row,
                        text=label,
                        font=("Segoe UI", 10, "bold"),
                        bg="#f9fafb",
                        fg="#374151",
                        width=15,
                        anchor="w"
                    ).pack(side="left")

                    tk.Label(
                        row,
                        text=value,
                        font=("Segoe UI", 10),
                        bg="#f9fafb",
                        fg="#6b7280"
                    ).pack(side="left")

                actions_row = tk.Frame(card_inner, bg="#f9fafb")
                actions_row.pack(fill="x", pady=(10, 0))

                def make_start_handler(booking_id: int):
                    def _handler():
                        try:
                            booking_service.start_ride(booking_id, self.user["id"])
                            messagebox.showinfo("Ride started", "Ride has been started successfully.")
                            self._show_assigned_trips()
                        except Exception as e:
                            messagebox.showerror("Error", f"Could not start ride: {e}")
                    return _handler

                def make_complete_handler(booking_id: int):
                    def _handler():
                        try:
                            booking_service.complete_ride(booking_id, self.user["id"])
                            messagebox.showinfo("Ride completed", "Ride has been completed successfully.")
                            self.user["status"] = "available"
                            self._build_dashboard()
                        except Exception as e:
                            messagebox.showerror("Error", f"Could not complete ride: {e}")
                    return _handler

                status = trip["status"]
                if status == "assigned":
                    tk.Button(
                        actions_row,
                        text="Start Ride",
                        font=("Segoe UI", 10, "bold"),
                        bg="#10b981",
                        fg="white",
                        activebackground="#059669",
                        activeforeground="white",
                        relief="flat",
                        cursor="hand2",
                        command=make_start_handler(trip["id"]),
                        padx=15,
                        pady=6,
                    ).pack(side="left")
                elif status == "ongoing":
                    tk.Button(
                        actions_row,
                        text="Complete Ride",
                        font=("Segoe UI", 10, "bold"),
                        bg="#3b82f6",
                        fg="white",
                        activebackground="#2563eb",
                        activeforeground="white",
                        relief="flat",
                        cursor="hand2",
                        command=make_complete_handler(trip["id"]),
                        padx=15,
                        pady=6,
                    ).pack(side="left")

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            tk.Button(
                trips_frame,
                text="Refresh Trips",
                font=("Segoe UI", 10),
                bg="#10b981",
                fg="white",
                activebackground="#059669",
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                command=self._show_assigned_trips,
                padx=15,
                pady=8
            ).pack(pady=(15, 0))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load trips: {e}")

    def _show_status_update(self):
        """Show status update form"""
        for widget in self.content_area.winfo_children():
            widget.destroy()

        status_frame = tk.Frame(self.content_area, bg="white")
        status_frame.pack(fill="both", expand=True, padx=40, pady=30)

        tk.Label(
            status_frame,
            text="Update Your Status",
            font=("Segoe UI", 18, "bold"),
            bg="white",
            fg="#1f2937"
        ).pack(anchor="w", pady=(0, 20))

        current_status = self.user.get('status', 'available')
        
        tk.Label(
            status_frame,
            text=f"Current Status: {current_status.upper()}",
            font=("Segoe UI", 12),
            bg="white",
            fg="#6b7280"
        ).pack(anchor="w", pady=(0, 30))

        status_var = tk.StringVar(value=current_status)

        statuses = [
            ("Available", "available", "#22c55e", "Ready to accept trips"),
            ("Busy", "busy", "#ef4444", "Currently on a trip"),
            ("Inactive", "inactive", "#6b7280", "Not accepting trips"),
        ]

        for label, value, color, desc in statuses:
            card = tk.Frame(status_frame, bg="#f9fafb", relief="solid", bd=1)
            card.pack(fill="x", pady=8)

            card_inner = tk.Frame(card, bg="#f9fafb")
            card_inner.pack(fill="both", expand=True, padx=20, pady=15)

            radio = tk.Radiobutton(
                card_inner,
                text=label,
                variable=status_var,
                value=value,
                font=("Segoe UI", 12, "bold"),
                bg="#f9fafb",
                fg="#1f2937",
                selectcolor="#f9fafb",
                activebackground="#f9fafb"
            )
            radio.pack(anchor="w")

            tk.Label(
                card_inner,
                text=desc,
                font=("Segoe UI", 10),
                bg="#f9fafb",
                fg="#6b7280"
            ).pack(anchor="w", padx=(25, 0))

        def update_status():
            new_status = status_var.get()
            try:
                driver_service = self.controller.context.driver_service
                driver_service.update_status(self.user['id'], new_status)
                self.user['status'] = new_status
                messagebox.showinfo("Success", f"Status updated to {new_status}")
                self._build_dashboard()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update status: {e}")

        tk.Button(
            status_frame,
            text="Update Status",
            font=("Segoe UI", 11, "bold"),
            bg="#10b981",
            fg="white",
            activebackground="#059669",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=update_status,
            pady=10
        ).pack(fill="x", pady=(25, 0))

    def _show_profile(self):
        """Show driver profile"""
        for widget in self.content_area.winfo_children():
            widget.destroy()

        profile_frame = tk.Frame(self.content_area, bg="white")
        profile_frame.pack(fill="both", expand=True, padx=40, pady=30)

        tk.Label(
            profile_frame,
            text="My Profile",
            font=("Segoe UI", 18, "bold"),
            bg="white",
            fg="#1f2937"
        ).pack(anchor="w", pady=(0, 20))

        info = [
            ("Full Name:", self.user.get('full_name', 'N/A')),
            ("Email:", self.user.get('email', 'N/A')),
            ("Phone:", self.user.get('phone', 'N/A')),
            ("Address:", self.user.get('address', 'N/A')),
            ("License Number:", self.user.get('license_number', 'N/A')),
            ("Vehicle Number:", self.user.get('vehicle_number', 'N/A')),
            ("Status:", self.user.get('status', 'N/A')),
            ("Username:", self.user.get('username', 'N/A')),
        ]

        for label, value in info:
            row = tk.Frame(profile_frame, bg="white")
            row.pack(fill="x", pady=8)

            tk.Label(
                row,
                text=label,
                font=("Segoe UI", 11, "bold"),
                bg="white",
                fg="#374151",
                width=18,
                anchor="w"
            ).pack(side="left")

            tk.Label(
                row,
                text=value,
                font=("Segoe UI", 11),
                bg="white",
                fg="#6b7280"
            ).pack(side="left")

    def _logout(self):
        """Logout user"""
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?"):
            self.controller.set_current_user(None)
            self.controller.show_frame("LoginPage")