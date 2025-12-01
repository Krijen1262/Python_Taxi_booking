# ui/admin_dashboard.py

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class AdminDashboard(tk.Frame):
    """
    Admin Dashboard with menu access to:
    - View All Bookings
    - Assign Drivers to Bookings
    - Manage Drivers
    - Manage Customers
    - System Overview
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

        # ===== HEADER =====
        header = tk.Frame(self.container, bg="#dc2626", height=80)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        header_content = tk.Frame(header, bg="#dc2626")
        header_content.pack(fill="both", expand=True, padx=30, pady=15)

        tk.Label(
            header_content,
            text=f"Admin Dashboard - {self.user.get('full_name', 'Administrator')}",
            font=("Segoe UI", 20, "bold"),
            bg="#dc2626",
            fg="white"
        ).pack(side="left")

        logout_btn = tk.Button(
            header_content,
            text="Logout",
            font=("Segoe UI", 10),
            bg="#7f1d1d",
            fg="white",
            activebackground="#991b1b",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self._logout,
            padx=20,
            pady=8
        )
        logout_btn.pack(side="right")

        # ===== MAIN CONTENT AREA =====
        main_content = tk.Frame(self.container, bg="#f8fafc")
        main_content.pack(fill="both", expand=True, padx=30, pady=20)

        # ===== LEFT SIDEBAR - MENU =====
        sidebar = tk.Frame(main_content, bg="white", width=250)
        sidebar.pack(side="left", fill="y", padx=(0, 20))
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="Admin Menu",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#1f2937"
        ).pack(pady=20)

        menu_items = [
            ("📊 Dashboard", self._show_overview),
            ("📋 All Bookings", self._show_all_bookings),
            ("🚗 Assign Drivers", self._show_assign_driver),
            ("👥 Manage Drivers", self._show_manage_drivers),
            ("👤 Manage Customers", self._show_manage_customers),
        ]

        for text, command in menu_items:
            btn = tk.Button(
                sidebar,
                text=text,
                font=("Segoe UI", 11),
                bg="white",
                fg="#374151",
                activebackground="#fee2e2",
                activeforeground="#dc2626",
                relief="flat",
                cursor="hand2",
                command=command,
                anchor="w",
                padx=20,
                pady=12
            )
            btn.pack(fill="x", padx=10, pady=2)

        # ===== RIGHT CONTENT AREA =====
        self.content_area = tk.Frame(main_content, bg="white")
        self.content_area.pack(side="right", fill="both", expand=True)

        # Show overview by default
        self._show_overview()

    def _show_overview(self):
        """Show system overview"""
        for widget in self.content_area.winfo_children():
            widget.destroy()

        overview_frame = tk.Frame(self.content_area, bg="white")
        overview_frame.pack(fill="both", expand=True, padx=40, pady=30)

        tk.Label(
            overview_frame,
            text="System Overview",
            font=("Segoe UI", 18, "bold"),
            bg="white",
            fg="#1f2937"
        ).pack(anchor="w", pady=(0, 30))

        # Get statistics
        try:
            booking_service = self.controller.context.booking_service
            driver_service = self.controller.context.driver_service
            customer_service = self.controller.context.customer_service

            total_bookings = len(booking_service.list_all())
            total_drivers = len(driver_service.list_all())
            total_customers = len(customer_service.list_all())
            available_drivers = len(driver_service.list_available())

            # Stats cards
            stats = [
                ("Total Bookings", total_bookings, "#667eea"),
                ("Total Drivers", total_drivers, "#10b981"),
                ("Total Customers", total_customers, "#f59e0b"),
                ("Available Drivers", available_drivers, "#22c55e"),
            ]

            cards_container = tk.Frame(overview_frame, bg="white")
            cards_container.pack(fill="x", pady=(0, 30))

            for i, (label, value, color) in enumerate(stats):
                card = tk.Frame(cards_container, bg=color, relief="solid", bd=0)
                card.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
                
                cards_container.grid_columnconfigure(0, weight=1)
                cards_container.grid_columnconfigure(1, weight=1)

                tk.Label(
                    card,
                    text=str(value),
                    font=("Segoe UI", 36, "bold"),
                    bg=color,
                    fg="white"
                ).pack(pady=(20, 5))

                tk.Label(
                    card,
                    text=label,
                    font=("Segoe UI", 12),
                    bg=color,
                    fg="white"
                ).pack(pady=(0, 20))

            # Recent bookings
            tk.Label(
                overview_frame,
                text="Recent Bookings",
                font=("Segoe UI", 14, "bold"),
                bg="white",
                fg="#1f2937"
            ).pack(anchor="w", pady=(20, 10))

            recent_bookings = booking_service.list_all()[-5:]  # Last 5 bookings
            
            if recent_bookings:
                for booking in reversed(recent_bookings):
                    card = tk.Frame(overview_frame, bg="#f9fafb", relief="solid", bd=1)
                    card.pack(fill="x", pady=5)

                    card_inner = tk.Frame(card, bg="#f9fafb")
                    card_inner.pack(fill="both", expand=True, padx=15, pady=10)

                    tk.Label(
                        card_inner,
                        text=f"Booking #{booking['id']} - {booking['pickup_location']} → {booking['dropoff_location']}",
                        font=("Segoe UI", 10),
                        bg="#f9fafb",
                        fg="#1f2937"
                    ).pack(side="left")

                    tk.Label(
                        card_inner,
                        text=booking['status'].upper(),
                        font=("Segoe UI", 9, "bold"),
                        bg="#667eea" if booking['status'] == 'pending' else "#10b981",
                        fg="white",
                        padx=8,
                        pady=2
                    ).pack(side="right")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load overview: {e}")

    def _show_all_bookings(self):
        """Show all bookings"""
        for widget in self.content_area.winfo_children():
            widget.destroy()

        bookings_frame = tk.Frame(self.content_area, bg="white")
        bookings_frame.pack(fill="both", expand=True, padx=40, pady=30)

        tk.Label(
            bookings_frame,
            text="All Bookings",
            font=("Segoe UI", 18, "bold"),
            bg="white",
            fg="#1f2937"
        ).pack(anchor="w", pady=(0, 20))

        try:
            booking_service = self.controller.context.booking_service
            bookings = booking_service.list_all()

            if not bookings:
                tk.Label(
                    bookings_frame,
                    text="No bookings found",
                    font=("Segoe UI", 12),
                    bg="white",
                    fg="#6b7280"
                ).pack(pady=50)
                return

            # Create table with scrollbar
            table_frame = tk.Frame(bookings_frame, bg="white")
            table_frame.pack(fill="both", expand=True)

            columns = ("ID", "Customer", "Pickup", "Dropoff", "Date", "Time", "Driver", "Status")
            tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)

            scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=90)

            for booking in bookings:
                values = (
                    booking['id'],
                    booking.get('customer_name', 'N/A'),
                    booking['pickup_location'],
                    booking['dropoff_location'],
                    booking['pickup_date'],
                    booking['pickup_time'],
                    booking.get('driver_name', 'Unassigned'),
                    booking['status']
                )
                tree.insert("", "end", values=values)

            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Action button
            tk.Button(
                bookings_frame,
                text="Refresh",
                font=("Segoe UI", 10),
                bg="#dc2626",
                fg="white",
                activebackground="#b91c1c",
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                command=self._show_all_bookings,
                padx=15,
                pady=8
            ).pack(pady=(15, 0))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load bookings: {e}")

    def _show_assign_driver(self):
        """Show driver assignment interface"""
        for widget in self.content_area.winfo_children():
            widget.destroy()

        assign_frame = tk.Frame(self.content_area, bg="white")
        assign_frame.pack(fill="both", expand=True, padx=40, pady=30)

        tk.Label(
            assign_frame,
            text="Assign Driver to Booking",
            font=("Segoe UI", 18, "bold"),
            bg="white",
            fg="#1f2937"
        ).pack(anchor="w", pady=(0, 20))

        try:
            booking_service = self.controller.context.booking_service
            driver_service = self.controller.context.driver_service

            # Get unassigned bookings
            all_bookings = booking_service.list_all()
            unassigned = [b for b in all_bookings if not b.get('driver_id')]

            if not unassigned:
                tk.Label(
                    assign_frame,
                    text="No unassigned bookings",
                    font=("Segoe UI", 12),
                    bg="white",
                    fg="#6b7280"
                ).pack(pady=50)
                return

            # Booking selection
            tk.Label(
                assign_frame,
                text="Select Booking:",
                font=("Segoe UI", 11, "bold"),
                bg="white",
                fg="#374151"
            ).pack(anchor="w", pady=(10, 5))

            booking_var = tk.StringVar()
            booking_combo = ttk.Combobox(
                assign_frame,
                textvariable=booking_var,
                state="readonly",
                font=("Segoe UI", 10),
                width=70
            )
            booking_values = [
                f"#{b['id']} - {b['pickup_location']} → {b['dropoff_location']} ({b['pickup_date']} {b['pickup_time']})"
                for b in unassigned
            ]
            booking_combo['values'] = booking_values
            booking_combo.pack(fill="x", pady=(0, 20))

            # Driver selection
            tk.Label(
                assign_frame,
                text="Select Available Driver:",
                font=("Segoe UI", 11, "bold"),
                bg="white",
                fg="#374151"
            ).pack(anchor="w", pady=(10, 5))

            driver_var = tk.StringVar()
            driver_combo = ttk.Combobox(
                assign_frame,
                textvariable=driver_var,
                state="readonly",
                font=("Segoe UI", 10),
                width=70
            )
            
            available_drivers = driver_service.list_available()
            driver_values = [
                f"#{d['id']} - {d['full_name']} (Vehicle: {d['vehicle_number']})"
                for d in available_drivers
            ]
            driver_combo['values'] = driver_values
            driver_combo.pack(fill="x", pady=(0, 30))

            def assign_driver():
                if not booking_var.get() or not driver_var.get():
                    messagebox.showwarning("Warning", "Please select both booking and driver")
                    return

                booking_id = int(booking_var.get().split('#')[1].split(' ')[0])
                driver_id = int(driver_var.get().split('#')[1].split(' ')[0])

                try:
                    booking_service.assign_driver(booking_id, driver_id)
                    messagebox.showinfo("Success", "Driver assigned successfully")
                    self._show_assign_driver()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to assign driver: {e}")

            tk.Button(
                assign_frame,
                text="Assign Driver",
                font=("Segoe UI", 11, "bold"),
                bg="#dc2626",
                fg="white",
                activebackground="#b91c1c",
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                command=assign_driver,
                pady=12
            ).pack(fill="x")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load assignment interface: {e}")

    def _show_manage_drivers(self):
        """Show driver management"""
        for widget in self.content_area.winfo_children():
            widget.destroy()

        drivers_frame = tk.Frame(self.content_area, bg="white")
        drivers_frame.pack(fill="both", expand=True, padx=40, pady=30)

        tk.Label(
            drivers_frame,
            text="Manage Drivers",
            font=("Segoe UI", 18, "bold"),
            bg="white",
            fg="#1f2937"
        ).pack(anchor="w", pady=(0, 20))

        try:
            driver_service = self.controller.context.driver_service
            drivers = driver_service.list_all()

            if not drivers:
                tk.Label(
                    drivers_frame,
                    text="No drivers found",
                    font=("Segoe UI", 12),
                    bg="white",
                    fg="#6b7280"
                ).pack(pady=50)
                return

            # Create table
            table_frame = tk.Frame(drivers_frame, bg="white")
            table_frame.pack(fill="both", expand=True)

            columns = ("ID", "Name", "Phone", "Email", "License", "Vehicle", "Status")
            tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)

            scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=90)

            for driver in drivers:
                values = (
                    driver['id'],
                    driver['full_name'],
                    driver['phone'],
                    driver['email'],
                    driver['license_number'],
                    driver['vehicle_number'],
                    driver['status']
                )
                tree.insert("", "end", values=values)

            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load drivers: {e}")

    def _show_manage_customers(self):
        """Show customer management"""
        for widget in self.content_area.winfo_children():
            widget.destroy()

        customers_frame = tk.Frame(self.content_area, bg="white")
        customers_frame.pack(fill="both", expand=True, padx=40, pady=30)

        tk.Label(
            customers_frame,
            text="Manage Customers",
            font=("Segoe UI", 18, "bold"),
            bg="white",
            fg="#1f2937"
        ).pack(anchor="w", pady=(0, 20))

        try:
            customer_service = self.controller.context.customer_service
            customers = customer_service.list_all()

            if not customers:
                tk.Label(
                    customers_frame,
                    text="No customers found",
                    font=("Segoe UI", 12),
                    bg="white",
                    fg="#6b7280"
                ).pack(pady=50)
                return

            # Create table
            table_frame = tk.Frame(customers_frame, bg="white")
            table_frame.pack(fill="both", expand=True)

            columns = ("ID", "Name", "Phone", "Email", "Address")
            tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)

            scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=120)

            for customer in customers:
                values = (
                    customer['id'],
                    customer['full_name'],
                    customer['phone'],
                    customer['email'],
                    customer['address']
                )
                tree.insert("", "end", values=values)

            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load customers: {e}")

    def _logout(self):
        """Logout user"""
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?"):
            self.controller.set_current_user(None)
            self.controller.show_frame("LoginPage")