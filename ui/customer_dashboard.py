# ui/customer_dashboard.py

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class CustomerDashboard(tk.Frame):
    """
    Customer Dashboard with menu access to:
    - Book a Taxi
    - View My Bookings
    - Update Booking
    - Cancel Booking
    - My Profile
    """

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f8fafc")
        self.controller = controller
        self.user = None

        # keep references to sidebar buttons for highlighting
        self.menu_buttons = []

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
        header = tk.Frame(self.container, bg="#667eea", height=70)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        header_content = tk.Frame(header, bg="#667eea")
        header_content.pack(fill="both", expand=True, padx=30, pady=10)

        # Left side - Title and user info
        left_header = tk.Frame(header_content, bg="#667eea")
        left_header.pack(side="left", fill="y")

        tk.Label(
            left_header,
            text="🚖 Taxi Booking System",
            font=("Segoe UI", 18, "bold"),
            bg="#667eea",
            fg="white"
        ).pack(anchor="w")

        tk.Label(
            left_header,
            text=f"Welcome, {self.user.get('full_name', 'Customer')}",
            font=("Segoe UI", 10),
            bg="#667eea",
            fg="#e0e7ff"
        ).pack(anchor="w")

        # Right side - Logout button
        logout_btn = tk.Button(
            header_content,
            text="🚪 Logout",
            font=("Segoe UI", 10, "bold"),
            bg="#ef4444",
            fg="white",
            activebackground="#dc2626",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self._logout,
            padx=20,
            pady=8,
            bd=0
        )
        logout_btn.pack(side="right")

        # ===== MAIN CONTENT AREA =====
        main_content = tk.Frame(self.container, bg="#f8fafc")
        main_content.pack(fill="both", expand=True, padx=20, pady=20)

        # ===== LEFT SIDEBAR - MENU =====
        sidebar = tk.Frame(main_content, bg="white", width=220, relief="solid", bd=1)
        sidebar.pack(side="left", fill="y", padx=(0, 15))
        sidebar.pack_propagate(False)

        # Menu header
        menu_header = tk.Frame(sidebar, bg="#667eea", height=50)
        menu_header.pack(fill="x")
        menu_header.pack_propagate(False)

        tk.Label(
            menu_header,
            text="📋 Menu",
            font=("Segoe UI", 14, "bold"),
            bg="#667eea",
            fg="white"
        ).pack(expand=True)

        # Menu items with icons
        menu_items = [
            ("🏠 Dashboard", self._show_welcome, "#667eea"),
            ("🚖 Book a Taxi", self._show_book_taxi, "#667eea"),
            ("📋 My Bookings", self._show_my_bookings, "#667eea"),
            ("✏️ Update Booking", self._show_update_booking, "#667eea"),
            ("👤 My Profile", self._show_profile, "#667eea"),
        ]

        self.menu_buttons = []
        for text, command, color in menu_items:
            # IMPORTANT: pass both the command function and this specific button
            btn = tk.Button(
                sidebar,
                text=text,
                font=("Segoe UI", 11),
                bg="white",
                fg="#374151",
                activebackground="#e0e7ff",
                activeforeground="#667eea",
                relief="flat",
                cursor="hand2",
                command=lambda c=command, b=None: self._handle_menu_click(c, b),
                anchor="w",
                padx=20,
                pady=15,
                bd=0
            )
            btn.pack(fill="x")
            # now that btn exists, re-bind its command so lambda captures THIS btn
            btn.config(command=lambda c=command, b=btn: self._handle_menu_click(c, b))
            self.menu_buttons.append(btn)

            # Add separator
            tk.Frame(sidebar, bg="#e5e7eb", height=1).pack(fill="x")

        # ===== RIGHT CONTENT AREA =====
        self.content_area = tk.Frame(main_content, bg="white", relief="solid", bd=1)
        self.content_area.pack(side="right", fill="both", expand=True)

        # Show welcome screen by default and highlight Dashboard in menu
        if self.menu_buttons:
            self._handle_menu_click(self._show_welcome, self.menu_buttons[0])
        else:
            self._show_welcome()

    def _handle_menu_click(self, command, active_button):
        """Handle menu item click with visual feedback and open the right page"""
        # Reset all buttons
        for btn in self.menu_buttons:
            btn.config(bg="white", fg="#374151")

        # Highlight clicked button
        if active_button is not None:
            active_button.config(bg="#e0e7ff", fg="#667eea")

        # Execute the page function (same functions used by dashboard buttons)
        command()

    # ------------------------------------------------------------------ #
    #  COMMON: CLEAR CONTENT
    # ------------------------------------------------------------------ #
    def _clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    # ------------------------------------------------------------------ #
    #  DASHBOARD / WELCOME
    # ------------------------------------------------------------------ #
    def _show_welcome(self):
        """Show welcome screen with quick stats"""
        self._clear_content()

        welcome_frame = tk.Frame(self.content_area, bg="white")
        welcome_frame.pack(fill="both", expand=True, padx=50, pady=40)

        # Welcome message
        tk.Label(
            welcome_frame,
            text="🚕",
            font=("Segoe UI", 70),
            bg="white"
        ).pack(pady=(20, 10))

        tk.Label(
            welcome_frame,
            text=f"Welcome back, {self.user.get('full_name', 'Customer')}!",
            font=("Segoe UI", 22, "bold"),
            bg="white",
            fg="#1f2937"
        ).pack()

        tk.Label(
            welcome_frame,
            text="Select an option from the menu to get started",
            font=("Segoe UI", 12),
            bg="white",
            fg="#6b7280"
        ).pack(pady=(5, 30))

        # Quick stats cards
        stats_frame = tk.Frame(welcome_frame, bg="white")
        stats_frame.pack(fill="x", pady=20)

        try:
            booking_service = self.controller.context.booking_service
            bookings = booking_service.get_customer_bookings(self.user['id'])

            pending = len([b for b in bookings if b['status'] == 'pending'])
            confirmed = len([b for b in bookings if b['status'] == 'confirmed'])
            total = len(bookings)

            stats = [
                ("Total Bookings", total, "#667eea"),
                ("Pending", pending, "#f59e0b"),
                ("Confirmed", confirmed, "#10b981"),
            ]

            for i, (label, value, color) in enumerate(stats):
                card = tk.Frame(stats_frame, bg=color, width=150, height=120)
                card.grid(row=0, column=i, padx=15, sticky="nsew")
                card.pack_propagate(False)

                stats_frame.grid_columnconfigure(i, weight=1)

                tk.Label(
                    card,
                    text=str(value),
                    font=("Segoe UI", 32, "bold"),
                    bg=color,
                    fg="white"
                ).pack(pady=(20, 5))

                tk.Label(
                    card,
                    text=label,
                    font=("Segoe UI", 11),
                    bg=color,
                    fg="white"
                ).pack()

        except Exception:
            tk.Label(
                welcome_frame,
                text=f"Could not load statistics",
                font=("Segoe UI", 10),
                bg="white",
                fg="#ef4444"
            ).pack()

        # Quick action buttons
        actions_frame = tk.Frame(welcome_frame, bg="white")
        actions_frame.pack(pady=30)

        tk.Button(
            actions_frame,
            text="🚖 Book a New Taxi",
            font=("Segoe UI", 12, "bold"),
            bg="#667eea",
            fg="white",
            activebackground="#5568d3",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self._show_book_taxi,
            padx=30,
            pady=12,
            bd=0
        ).pack(side="left", padx=10)

        tk.Button(
            actions_frame,
            text="📋 View My Bookings",
            font=("Segoe UI", 12, "bold"),
            bg="#10b981",
            fg="white",
            activebackground="#059669",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self._show_my_bookings,
            padx=30,
            pady=12,
            bd=0
        ).pack(side="left", padx=10)

    # ------------------------------------------------------------------ #
    #  BOOK TAXI
    # ------------------------------------------------------------------ #
    def _show_book_taxi(self):
        """Show book taxi form"""
        self._clear_content()

        form_container = tk.Frame(self.content_area, bg="white")
        form_container.pack(fill="both", expand=True)

        # Header
        header = tk.Frame(form_container, bg="#667eea", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🚖 Book a Taxi",
            font=("Segoe UI", 18, "bold"),
            bg="#667eea",
            fg="white"
        ).pack(side="left", padx=30, pady=15)

        # Form
        form_frame = tk.Frame(form_container, bg="white")
        form_frame.pack(fill="both", expand=True, padx=50, pady=30)

        # Pickup Location
        tk.Label(
            form_frame,
            text="Pickup Location *",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#374151",
            anchor="w"
        ).pack(fill="x", pady=(10, 5))

        pickup_entry = tk.Entry(
            form_frame,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1,
            highlightthickness=2,
            highlightcolor="#667eea",
            highlightbackground="#e5e7eb"
        )
        pickup_entry.pack(fill="x", ipady=10)

        # Drop-off Location
        tk.Label(
            form_frame,
            text="Drop-off Location *",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#374151",
            anchor="w"
        ).pack(fill="x", pady=(20, 5))

        dropoff_entry = tk.Entry(
            form_frame,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1,
            highlightthickness=2,
            highlightcolor="#667eea",
            highlightbackground="#e5e7eb"
        )
        dropoff_entry.pack(fill="x", ipady=10)

        # Date and Time in one row
        datetime_frame = tk.Frame(form_frame, bg="white")
        datetime_frame.pack(fill="x", pady=(20, 0))

        # Date
        date_col = tk.Frame(datetime_frame, bg="white")
        date_col.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(
            date_col,
            text="Pickup Date *",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#374151",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))

        date_entry = tk.Entry(
            date_col,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1,
            highlightthickness=2,
            highlightcolor="#667eea",
            highlightbackground="#e5e7eb"
        )
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_entry.pack(fill="x", ipady=10)

        # Time
        time_col = tk.Frame(datetime_frame, bg="white")
        time_col.pack(side="left", fill="both", expand=True, padx=(10, 0))

        tk.Label(
            time_col,
            text="Pickup Time *",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#374151",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))

        time_entry = tk.Entry(
            time_col,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1,
            highlightthickness=2,
            highlightcolor="#667eea",
            highlightbackground="#e5e7eb"
        )
        time_entry.insert(0, datetime.now().strftime("%H:%M"))
        time_entry.pack(fill="x", ipady=10)

        # Submit button
        def submit_booking():
            pickup = pickup_entry.get().strip()
            dropoff = dropoff_entry.get().strip()
            date = date_entry.get().strip()
            time = time_entry.get().strip()

            if not all([pickup, dropoff, date, time]):
                messagebox.showerror("Error", "All fields are required")
                return

            try:
                booking_service = self.controller.context.booking_service
                # Combine date and time into datetime string format "YYYY-MM-DD HH:MM"
                pickup_datetime_str = f"{date} {time}"
                booking_id = booking_service.create_booking_for_customer(
                    customer_id=self.user['id'],
                    pickup_location=pickup,
                    dropoff_location=dropoff,
                    pickup_datetime_str=pickup_datetime_str
                )
                messagebox.showinfo(
                    "Success",
                    f"Booking created successfully!\nBooking ID: {booking_id}"
                )

                # Clear form
                pickup_entry.delete(0, tk.END)
                dropoff_entry.delete(0, tk.END)
                date_entry.delete(0, tk.END)
                date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
                time_entry.delete(0, tk.END)
                time_entry.insert(0, datetime.now().strftime("%H:%M"))

                self._show_my_bookings()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create booking: {e}")

        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.pack(fill="x", pady=(30, 0))

        tk.Button(
            btn_frame,
            text="📝 Create Booking",
            font=("Segoe UI", 12, "bold"),
            bg="#667eea",
            fg="white",
            activebackground="#5568d3",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=submit_booking,
            pady=12,
            bd=0
        ).pack(side="left", fill="x", expand=True, padx=(0, 10))

        tk.Button(
            btn_frame,
            text="🔄 Clear Form",
            font=("Segoe UI", 12),
            bg="#e5e7eb",
            fg="#374151",
            activebackground="#d1d5db",
            activeforeground="#1f2937",
            relief="flat",
            cursor="hand2",
            command=lambda: [
                pickup_entry.delete(0, tk.END),
                dropoff_entry.delete(0, tk.END)
            ],
            pady=12,
            bd=0
        ).pack(side="left", fill="x", expand=True, padx=(10, 0))

    # ------------------------------------------------------------------ #
    #  MY BOOKINGS
    # ------------------------------------------------------------------ #
    def _show_my_bookings(self):
        """Show customer's bookings"""
        self._clear_content()

        bookings_container = tk.Frame(self.content_area, bg="white")
        bookings_container.pack(fill="both", expand=True)

        # Header
        header = tk.Frame(bookings_container, bg="#667eea", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="📋 My Bookings",
            font=("Segoe UI", 18, "bold"),
            bg="#667eea",
            fg="white"
        ).pack(side="left", padx=30, pady=15)

        tk.Button(
            header,
            text="🔄 Refresh",
            font=("Segoe UI", 10),
            bg="#5568d3",
            fg="white",
            activebackground="#4c51bf",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self._show_my_bookings,
            padx=15,
            pady=6,
            bd=0
        ).pack(side="right", padx=30)

        # Content
        bookings_frame = tk.Frame(bookings_container, bg="white")
        bookings_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # Get bookings
        try:
            booking_service = self.controller.context.booking_service
            bookings = booking_service.get_customer_bookings(self.user['id'])

            if not bookings:
                empty_frame = tk.Frame(bookings_frame, bg="white")
                empty_frame.place(relx=0.5, rely=0.5, anchor="c")

                tk.Label(
                    empty_frame,
                    text="📭",
                    font=("Segoe UI", 60),
                    bg="white"
                ).pack()

                tk.Label(
                    empty_frame,
                    text="No bookings found",
                    font=("Segoe UI", 14, "bold"),
                    bg="white",
                    fg="#6b7280"
                ).pack(pady=10)

                tk.Button(
                    empty_frame,
                    text="Book Your First Taxi",
                    font=("Segoe UI", 11),
                    bg="#667eea",
                    fg="white",
                    activebackground="#5568d3",
                    activeforeground="white",
                    relief="flat",
                    cursor="hand2",
                    command=self._show_book_taxi,
                    padx=20,
                    pady=10,
                    bd=0
                ).pack(pady=10)
                return

            # Create styled table
            style = ttk.Style()
            style.theme_use('clam')
            style.configure(
                "Treeview",
                background="white",
                foreground="#1f2937",
                rowheight=30,
                fieldbackground="white",
                borderwidth=0,
                font=("Segoe UI", 10)
            )
            style.configure(
                "Treeview.Heading",
                background="#667eea",
                foreground="white",
                relief="flat",
                font=("Segoe UI", 10, "bold")
            )
            style.map('Treeview', background=[('selected', '#e0e7ff')])

            # Table frame
            table_frame = tk.Frame(bookings_frame, bg="white")
            table_frame.pack(fill="both", expand=True)

            columns = ("ID", "Pickup", "Dropoff", "Date", "Time", "Status")
            tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

            # Configure columns
            tree.column("ID", width=50, anchor="center")
            tree.column("Pickup", width=150)
            tree.column("Dropoff", width=150)
            tree.column("Date", width=100, anchor="center")
            tree.column("Time", width=80, anchor="center")
            tree.column("Status", width=100, anchor="center")

            for col in columns:
                tree.heading(col, text=col)

            # Add scrollbar
            scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)

            for booking in bookings:
                values = (
                    booking['id'],
                    booking['pickup_location'],
                    booking['dropoff_location'],
                    booking['pickup_date'],
                    booking['pickup_time'],
                    booking['status'].upper()
                )
                tree.insert("", "end", values=values, tags=(booking['id'],))

            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Action buttons
            btn_frame = tk.Frame(bookings_frame, bg="white")
            btn_frame.pack(fill="x", pady=(15, 0))

            def cancel_booking():
                selection = tree.selection()
                if not selection:
                    messagebox.showwarning("Warning", "Please select a booking to cancel")
                    return

                booking_id = tree.item(selection[0])['values'][0]

                if messagebox.askyesno("Confirm Cancellation", "Are you sure you want to cancel this booking?"):
                    try:
                        booking_service.cancel_booking(booking_id, self.user['id'])
                        messagebox.showinfo("Success", "Booking cancelled successfully")
                        self._show_my_bookings()
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to cancel booking: {e}")

            tk.Button(
                btn_frame,
                text="❌ Cancel Selected",
                font=("Segoe UI", 11),
                bg="#ef4444",
                fg="white",
                activebackground="#dc2626",
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                command=cancel_booking,
                padx=20,
                pady=10,
                bd=0
            ).pack(side="left")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load bookings: {e}")

    # ------------------------------------------------------------------ #
    #  UPDATE BOOKING (still placeholder UI – same as your original)
    # ------------------------------------------------------------------ #
    def _show_update_booking(self):
        """Show update booking interface"""
        self._clear_content()

        update_container = tk.Frame(self.content_area, bg="white")
        update_container.pack(fill="both", expand=True)

        # Header
        header = tk.Frame(update_container, bg="#667eea", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="✏️ Update Booking",
            font=("Segoe UI", 18, "bold"),
            bg="#667eea",
            fg="white"
        ).pack(side="left", padx=30, pady=15)

        # Content
        update_frame = tk.Frame(update_container, bg="white")
        update_frame.pack(fill="both", expand=True, padx=50, pady=30)

        tk.Label(
            update_frame,
            text="Select a booking from 'My Bookings' to update",
            font=("Segoe UI", 12),
            bg="white",
            fg="#6b7280"
        ).pack(pady=50)

        tk.Label(
            update_frame,
            text="📝",
            font=("Segoe UI", 60),
            bg="white"
        ).pack()

        tk.Label(
            update_frame,
            text="Update feature coming soon!",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#374151"
        ).pack(pady=20)

    # ------------------------------------------------------------------ #
    #  PROFILE
    # ------------------------------------------------------------------ #
    def _show_profile(self):
        """Show user profile"""
        self._clear_content()

        profile_container = tk.Frame(self.content_area, bg="white")
        profile_container.pack(fill="both", expand=True)

        # Header
        header = tk.Frame(profile_container, bg="#667eea", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="👤 My Profile",
            font=("Segoe UI", 18, "bold"),
            bg="#667eea",
            fg="white"
        ).pack(side="left", padx=30, pady=15)

        # Profile content
        profile_frame = tk.Frame(profile_container, bg="white")
        profile_frame.pack(fill="both", expand=True, padx=50, pady=30)

        # Profile card
        card = tk.Frame(profile_frame, bg="#f9fafb", relief="solid", bd=1)
        card.pack(fill="both", expand=True)

        card_inner = tk.Frame(card, bg="#f9fafb")
        card_inner.pack(fill="both", expand=True, padx=40, pady=30)

        # Profile icon
        tk.Label(
            card_inner,
            text="👤",
            font=("Segoe UI", 60),
            bg="#f9fafb"
        ).pack(pady=(0, 20))

        # Profile info
        info = [
            ("Full Name", self.user.get('full_name', 'N/A')),
            ("Email", self.user.get('email', 'N/A')),
            ("Phone", self.user.get('phone', 'N/A')),
            ("Address", self.user.get('address', 'N/A')),
            ("Username", self.user.get('username', 'N/A')),
            ("Customer ID", self.user.get('id', 'N/A')),
        ]

        for label, value in info:
            row_frame = tk.Frame(card_inner, bg="#f9fafb")
            row_frame.pack(fill="x", pady=8)

            tk.Label(
                row_frame,
                text=f"{label}:",
                font=("Segoe UI", 11, "bold"),
                bg="#f9fafb",
                fg="#374151",
                width=15,
                anchor="w"
            ).pack(side="left")

            tk.Label(
                row_frame,
                text=value,
                font=("Segoe UI", 11),
                bg="#f9fafb",
                fg="#6b7280"
            ).pack(side="left", padx=10)

    # ------------------------------------------------------------------ #
    #  LOGOUT
    # ------------------------------------------------------------------ #
    def _logout(self):
        """Logout user"""
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?"):
            self.controller.set_current_user(None)
            self.controller.show_frame("LoginPage")
