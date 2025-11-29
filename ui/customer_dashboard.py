# app/ui/customer_dashboard.py

import tkinter as tk
from tkinter import messagebox


class CustomerDashboard(tk.Frame):
    """
    Customer dashboard:
    - View own bookings
    - Create new booking
    - Update existing booking (only pending)
    - Cancel booking
    Uses BookingService via controller.context.booking_service
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.user = None  # logged-in user dict
        self.customer_id = None
        self.bookings = []  # cache of current bookings list

        # ===== HEADER =====
        header_frame = tk.Frame(self)
        header_frame.pack(fill="x", pady=10)

        self.header_label = tk.Label(
            header_frame, text="Customer Dashboard", font=("Arial", 20, "bold")
        )
        self.header_label.pack(side="left", padx=20)

        self.info_label = tk.Label(header_frame, text="", font=("Arial", 11))
        self.info_label.pack(side="right", padx=20)

        # ===== MAIN CONTENT =====
        content = tk.Frame(self)
        content.pack(fill="both", expand=True, padx=20, pady=10)

        # Left: Booking form
        form_frame = tk.LabelFrame(content, text="Booking Form", padx=10, pady=10)
        form_frame.pack(side="left", fill="y", padx=10, pady=5)

        tk.Label(form_frame, text="Pickup Location:", font=("Arial", 11)).grid(
            row=0, column=0, sticky="e", padx=5, pady=5
        )
        tk.Label(form_frame, text="Drop-off Location:", font=("Arial", 11)).grid(
            row=1, column=0, sticky="e", padx=5, pady=5
        )
        tk.Label(
            form_frame,
            text="Pickup Datetime\n(YYYY-MM-DD HH:MM):",
            font=("Arial", 11),
        ).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        tk.Label(form_frame, text="Notes (optional):", font=("Arial", 11)).grid(
            row=3, column=0, sticky="ne", padx=5, pady=5
        )

        self.entry_pickup = tk.Entry(form_frame, width=30)
        self.entry_dropoff = tk.Entry(form_frame, width=30)
        self.entry_datetime = tk.Entry(form_frame, width=30)
        self.text_notes = tk.Text(form_frame, width=30, height=4)

        self.entry_pickup.grid(row=0, column=1, padx=5, pady=5)
        self.entry_dropoff.grid(row=1, column=1, padx=5, pady=5)
        self.entry_datetime.grid(row=2, column=1, padx=5, pady=5)
        self.text_notes.grid(row=3, column=1, padx=5, pady=5)

        # Selected booking ID for update/cancel
        self.selected_booking_id = None
        self.selected_status = None

        button_frame = tk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        tk.Button(
            button_frame,
            text="Create Booking",
            width=15,
            command=self.handle_create_booking,
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="Update Selected",
            width=15,
            command=self.handle_update_booking,
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="Clear Form",
            width=15,
            command=self.clear_form,
        ).grid(row=1, column=0, padx=5, pady=5)

        tk.Button(
            button_frame,
            text="Cancel Selected",
            width=15,
            command=self.handle_cancel_booking,
        ).grid(row=1, column=1, padx=5, pady=5)

        # Right: Bookings list
        list_frame = tk.LabelFrame(content, text="My Bookings", padx=10, pady=10)
        list_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)

        self.listbox = tk.Listbox(list_frame, width=70, height=20)
        self.listbox.pack(side="left", fill="both", expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.on_booking_select)

        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        bottom_btn_frame = tk.Frame(self)
        bottom_btn_frame.pack(pady=10)

        tk.Button(
            bottom_btn_frame,
            text="Refresh Bookings",
            width=18,
            command=self.load_bookings,
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            bottom_btn_frame, text="Logout", width=10, command=self.controller.logout
        ).grid(row=0, column=1, padx=5)

    # ===== PUBLIC METHOD CALLED FROM LOGIN PAGE =====

    def set_user(self, user: dict):
        """
        Called by LoginPage after successful login.
        """
        self.user = user
        self.customer_id = user.get("customer_id")
        self.info_label.config(
            text=f"Logged in as: {user['username']} (Customer ID: {self.customer_id})"
        )
        # Load bookings for this customer
        self.load_bookings()
        self.clear_form()

    # ===== INTERNAL HELPERS =====

    def get_booking_service(self):
        return self.controller.context.booking_service

    def clear_form(self):
        self.entry_pickup.delete(0, tk.END)
        self.entry_dropoff.delete(0, tk.END)
        self.entry_datetime.delete(0, tk.END)
        self.text_notes.delete("1.0", tk.END)
        self.selected_booking_id = None
        self.selected_status = None

    def load_bookings(self):
        """
        Load bookings for the current customer and display in the listbox.
        """
        if not self.customer_id:
            return

        booking_service = self.get_booking_service()
        try:
            self.bookings = booking_service.get_customer_bookings(self.customer_id)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load bookings: {e}")
            return

        self.listbox.delete(0, tk.END)

        if not self.bookings:
            self.listbox.insert(tk.END, "No bookings found.")
            return

        for b in self.bookings:
            line = (
                f"ID {b['id']} | "
                f"{b['pickup_location']} -> {b['dropoff_location']} | "
                f"{b['pickup_datetime']} | "
                f"Status: {b['status']} | Driver: {b.get('driver_id')}"
            )
            self.listbox.insert(tk.END, line)

    def get_selected_booking(self):
        """
        Return the selected booking dict from self.bookings, or None.
        """
        if not self.bookings:
            return None

        selection = self.listbox.curselection()
        if not selection:
            return None

        index = selection[0]
        # If we inserted "No bookings found.", guard against that
        if index >= len(self.bookings):
            return None

        return self.bookings[index]

    # ===== EVENT HANDLERS =====

    def on_booking_select(self, event):
        """
        When user selects a booking in the list, load it into the form.
        """
        booking = self.get_selected_booking()
        if not booking:
            return

        self.selected_booking_id = booking["id"]
        self.selected_status = booking["status"]

        # Fill form with booking data
        self.entry_pickup.delete(0, tk.END)
        self.entry_pickup.insert(0, booking["pickup_location"])

        self.entry_dropoff.delete(0, tk.END)
        self.entry_dropoff.insert(0, booking["dropoff_location"])

        self.entry_datetime.delete(0, tk.END)
        # booking["pickup_datetime"] is a datetime; convert to string
        dt_str = str(booking["pickup_datetime"]).split(".")[0]  # remove microseconds
        self.entry_datetime.insert(0, dt_str)

        self.text_notes.delete("1.0", tk.END)
        if booking.get("notes"):
            self.text_notes.insert("1.0", booking["notes"])

    def handle_create_booking(self):
        """
        Create a new booking using the form fields.
        """
        if not self.customer_id:
            messagebox.showerror("Error", "No customer ID found for this user.")
            return

        pickup = self.entry_pickup.get().strip()
        dropoff = self.entry_dropoff.get().strip()
        pickup_dt = self.entry_datetime.get().strip()
        notes = self.text_notes.get("1.0", tk.END).strip()
        notes = notes if notes else None

        if not pickup or not dropoff or not pickup_dt:
            messagebox.showerror(
                "Error", "Pickup, Drop-off and Datetime are required."
            )
            return

        booking_service = self.get_booking_service()

        try:
            booking_id = booking_service.create_booking_for_customer(
                customer_id=self.customer_id,
                pickup_location=pickup,
                dropoff_location=dropoff,
                pickup_datetime_str=pickup_dt,
                notes=notes,
            )
            messagebox.showinfo(
                "Success", f"Booking created successfully. ID: {booking_id}"
            )
            self.clear_form()
            self.load_bookings()
        except Exception as e:
            messagebox.showerror("Error", f"Could not create booking: {e}")

    def handle_update_booking(self):
        """
        Update the selected booking with the data from the form.
        Only 'pending' bookings can be updated.
        """
        if self.selected_booking_id is None:
            messagebox.showerror("Error", "Please select a booking to update.")
            return

        if self.selected_status != "pending":
            messagebox.showerror(
                "Error", "Only 'pending' bookings can be updated from here."
            )
            return

        pickup = self.entry_pickup.get().strip()
        dropoff = self.entry_dropoff.get().strip()
        pickup_dt = self.entry_datetime.get().strip()
        notes = self.text_notes.get("1.0", tk.END).strip()
        notes = notes if notes else None

        if not pickup or not dropoff or not pickup_dt:
            messagebox.showerror(
                "Error", "Pickup, Drop-off and Datetime are required."
            )
            return

        booking_service = self.get_booking_service()

        try:
            booking_service.update_booking(
                booking_id=self.selected_booking_id,
                customer_id=self.customer_id,
                pickup_location=pickup,
                dropoff_location=dropoff,
                pickup_datetime_str=pickup_dt,
                notes=notes,
            )
            messagebox.showinfo("Success", "Booking updated successfully.")
            self.clear_form()
            self.load_bookings()
        except Exception as e:
            messagebox.showerror("Error", f"Could not update booking: {e}")

    def handle_cancel_booking(self):
        """
        Cancel the selected booking.
        """
        if self.selected_booking_id is None:
            messagebox.showerror("Error", "Please select a booking to cancel.")
            return

        confirm = messagebox.askyesno(
            "Confirm Cancel", "Are you sure you want to cancel this booking?"
        )
        if not confirm:
            return

        booking_service = self.get_booking_service()

        try:
            booking_service.cancel_booking(
                booking_id=self.selected_booking_id, customer_id=self.customer_id
            )
            messagebox.showinfo("Success", "Booking cancelled successfully.")
            self.clear_form()
            self.load_bookings()
        except Exception as e:
            messagebox.showerror("Error", f"Could not cancel booking: {e}")
