# ui/login_page.py

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # pip install pillow


class LoginPage(tk.Frame):
    """
    Login screen. On success:
    - sets controller.current_user
    - navigates to CustomerDashboard / DriverDashboard / AdminDashboard
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller  # MainApp instance

        # ----- BACKGROUND IMAGE -----
        # Change this path to your own image if needed
        image_path = "assets/register_bg.jpg"

        try:
            bg_img = Image.open(image_path)
            # Resize to match main window size (900x600)
            bg_img = bg_img.resize((900, 600), Image.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(bg_img)

            bg_label = tk.Label(self, image=self.bg_image)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception:
            # Fallback to a solid colour if image not found
            self.configure(bg="#eef2ff")

        # ----- CARD CONTAINER -----
        card = tk.Frame(
            self,
            bg="white",
            bd=0,
            highlightthickness=0,
        )
        # Center card
        card.place(relx=0.5, rely=0.5, anchor="c")

        inner = tk.Frame(card, bg="white")
        inner.pack(padx=40, pady=30)

        # ----- TITLE -----
        title = tk.Label(
            inner,
            text="Login",
            font=("Segoe UI", 22, "bold"),
            bg="white",
            fg="#1f2933",
        )
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # ----- FORM FIELDS -----
        labels = [
            "Username:",
            "Password:",
        ]

        self.entries = {}

        for i, text in enumerate(labels, start=1):
            tk.Label(
                inner,
                text=text,
                font=("Segoe UI", 11),
                bg="white",
                fg="#4b5563",
            ).grid(row=i, column=0, sticky="e", padx=(0, 10), pady=6)

            show_char = "*" if "Password" in text else ""
            entry = tk.Entry(
                inner,
                width=30,
                show=show_char,
                font=("Segoe UI", 10),
                relief="solid",
                bd=1,
            )
            entry.grid(row=i, column=1, padx=(0, 5), pady=6)
            self.entries[text] = entry

        # ----- BUTTONS -----
        btn_row = len(labels) + 1

        login_btn = tk.Button(
            inner,
            text="Login",
            width=14,
            font=("Segoe UI", 10, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.handle_login,
        )
        login_btn.grid(row=btn_row, column=0, pady=(20, 0), sticky="e")

        register_btn = tk.Button(
            inner,
            text="Register as Customer",
            width=14,
            font=("Segoe UI", 10),
            bg="#e5e7eb",
            fg="#111827",
            activebackground="#d1d5db",
            activeforeground="#111827",
            relief="flat",
            cursor="hand2",
            command=lambda: self.controller.show_frame("RegisterPage"),
        )
        register_btn.grid(row=btn_row, column=1, pady=(20, 0), sticky="w", padx=(10, 0))

    # ----- LOGIC -----

    def handle_login(self):
        username = self.entries["Username:"].get().strip()
        password = self.entries["Password:"].get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        user_service = self.controller.context.user_service
        user = user_service.login(username, password)

        if not user:
            messagebox.showerror(
                "Login failed", "Invalid credentials or inactive account."
            )
            return

        self.controller.set_current_user(user)

        role = user["role"]
        if role == "customer":
            customer_dash = self.controller.frames["CustomerDashboard"]
            customer_dash.set_user(user)
            self.controller.show_frame("CustomerDashboard")
        elif role == "driver":
            driver_dash = self.controller.frames["DriverDashboard"]
            driver_dash.set_user(user)
            self.controller.show_frame("DriverDashboard")
        elif role == "admin":
            admin_dash = self.controller.frames["AdminDashboard"]
            admin_dash.set_user(user)
            self.controller.show_frame("AdminDashboard")
        else:
            messagebox.showerror("Error", f"Unknown role: {role}")
