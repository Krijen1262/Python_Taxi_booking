# ui/register_page.py

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk


class RegisterPage(tk.Frame):
    """
    Enhanced customer registration page with gradient background and side image.
    Uses UserService from controller.context to create a new customer + user.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # ===== GRADIENT BACKGROUND =====
        self.configure(bg="#764ba2")
        
        # Bind to window resize to redraw gradient
        self.bind("<Configure>", self._on_resize)
        
        # Create canvas for gradient effect
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # ===== MAIN CONTAINER =====
        self.main_container = tk.Frame(self.canvas, bg="white")
        self.main_container.place(relx=0.5, rely=0.5, anchor="c", width=820, height=550)

        # ===== LEFT SIDE - FORM =====
        self.left_frame = tk.Frame(self.main_container, bg="white", width=500)
        self.left_frame.pack(side="left", fill="both", expand=False)
        self.left_frame.pack_propagate(False)

        # Inner container with padding
        form_outer = tk.Frame(self.left_frame, bg="white")
        form_outer.pack(fill="both", expand=True, padx=30, pady=20)

        # ===== TITLE =====
        title = tk.Label(
            form_outer,
            text="Create Account",
            font=("Segoe UI", 24, "bold"),
            bg="white",
            fg="#1a202c",
        )
        title.pack(pady=(0, 5))

        subtitle = tk.Label(
            form_outer,
            text="Join us today!",
            font=("Segoe UI", 11),
            bg="white",
            fg="#718096",
        )
        subtitle.pack(pady=(0, 15))

        # ===== SCROLLABLE FORM =====
        canvas_frame = tk.Frame(form_outer, bg="white")
        canvas_frame.pack(fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical")
        form_canvas = tk.Canvas(canvas_frame, bg="white", yscrollcommand=scrollbar.set, highlightthickness=0)
        scrollbar.config(command=form_canvas.yview)
        
        scrollbar.pack(side="right", fill="y")
        form_canvas.pack(side="left", fill="both", expand=True)
        
        # Form container inside canvas
        form_frame = tk.Frame(form_canvas, bg="white")
        form_canvas_window = form_canvas.create_window((0, 0), window=form_frame, anchor="nw")
        
        # Update scroll region when form changes size
        def configure_scroll(event):
            form_canvas.configure(scrollregion=form_canvas.bbox("all"))
            form_canvas.itemconfig(form_canvas_window, width=event.width)
        
        form_frame.bind("<Configure>", configure_scroll)
        form_canvas.bind("<Configure>", lambda e: form_canvas.itemconfig(form_canvas_window, width=e.width))

        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            form_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        form_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # ===== FORM FIELDS =====
        self.entries = {}

        # User Type Dropdown
        tk.Label(
            form_frame,
            text="User Type",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#4a5568",
            anchor="w"
        ).pack(fill="x", pady=(8, 3), padx=5)

        self.user_type_var = tk.StringVar(value="customer")
        user_type_combo = ttk.Combobox(
            form_frame,
            textvariable=self.user_type_var,
            values=["customer", "driver", "admin"],
            state="readonly",
            font=("Segoe UI", 10),
            width=38
        )
        user_type_combo.pack(fill="x", ipady=6, padx=5)
        user_type_combo.bind("<<ComboboxSelected>>", self._on_user_type_change)

        # Container for dynamic fields
        self.dynamic_fields_frame = tk.Frame(form_frame, bg="white")
        self.dynamic_fields_frame.pack(fill="both", expand=True)

        # Create initial fields for customer
        self._create_fields_for_type("customer")

        # ===== BUTTONS =====
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.pack(fill="x", pady=(20, 10), padx=5)

        register_btn = tk.Button(
            btn_frame,
            text="Register",
            font=("Segoe UI", 11, "bold"),
            bg="#764ba2",
            fg="white",
            activebackground="#653a8f",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.handle_register,
            bd=0
        )
        register_btn.pack(fill="x", ipady=10, pady=(0, 10))

        back_btn = tk.Button(
            btn_frame,
            text="← Back to Login",
            font=("Segoe UI", 10),
            bg="#f7fafc",
            fg="#764ba2",
            activebackground="#edf2f7",
            activeforeground="#653a8f",
            relief="solid",
            bd=1,
            cursor="hand2",
            command=lambda: self.controller.show_frame("LoginPage"),
        )
        back_btn.pack(fill="x", ipady=8)

        # ===== RIGHT SIDE - IMAGE SECTION =====
        self.right_frame = tk.Frame(self.main_container, bg="#764ba2", width=320)
        self.right_frame.pack(side="right", fill="both", expand=False)
        self.right_frame.pack_propagate(False)

        # Try to load decorative image
        self.side_image = None
        try:
            img = Image.open("assets/register_image.jpg")
            self._load_side_image()
        except Exception:
            # Fallback decorative content
            self._create_fallback_content()

    def _on_resize(self, event=None):
        """Handle window resize to redraw gradient"""
        self.after(10, self._draw_gradient)

    def _draw_gradient(self):
        """Draw a gradient background on canvas"""
        self.canvas.delete("gradient")
        width = self.canvas.winfo_width() or 900
        height = self.canvas.winfo_height() or 600
        
        # Gradient from purple to pink-purple
        step = max(1, height // 100)
        for i in range(0, height, step):
            ratio = i / height
            r = int(118 + (247 - 118) * ratio)
            g = int(75 + (167 - 75) * ratio)
            b = int(162 + (216 - 162) * ratio)
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_rectangle(0, i, width, i + step, fill=color, outline=color, tags="gradient")

    def _create_fallback_content(self):
        """Create fallback decorative content when image not found"""
        deco_frame = tk.Frame(self.right_frame, bg="#764ba2")
        deco_frame.place(relx=0.5, rely=0.5, anchor="c")
        
        tk.Label(
            deco_frame,
            text="🚕",
            font=("Segoe UI", 70),
            bg="#764ba2",
            fg="white"
        ).pack(pady=15)
        
        tk.Label(
            deco_frame,
            text="Start Your",
            font=("Segoe UI", 18, "bold"),
            bg="#764ba2",
            fg="white"
        ).pack()
        
        tk.Label(
            deco_frame,
            text="Journey",
            font=("Segoe UI", 18, "bold"),
            bg="#764ba2",
            fg="white"
        ).pack(pady=(0, 15))
        
        features = [
            "✓ Easy booking",
            "✓ 24/7 service",
            "✓ Safe rides",
            "✓ Best rates"
        ]
        
        for feature in features:
            tk.Label(
                deco_frame,
                text=feature,
                font=("Segoe UI", 11),
                bg="#764ba2",
                fg="white",
                anchor="w"
            ).pack(pady=5, padx=30, fill="x")

    def _on_user_type_change(self, event=None):
        """Handle user type selection change"""
        user_type = self.user_type_var.get()
        self._create_fields_for_type(user_type)

    def _create_fields_for_type(self, user_type):
        """Create form fields based on selected user type"""
        # Clear existing fields
        for widget in self.dynamic_fields_frame.winfo_children():
            widget.destroy()
        
        self.entries = {}
        
        # Define fields based on user type
        if user_type == "customer":
            fields = [
                ("Full Name", False),
                ("Address", False),
                ("Phone", False),
                ("Email", False),
                ("Username", False),
                ("Password", True),
                ("Confirm Password", True),
            ]
        elif user_type == "driver":
            fields = [
                ("Full Name", False),
                ("Address", False),
                ("Phone", False),
                ("Email", False),
                ("License Number", False),
                ("Vehicle Number", False),
                ("Username", False),
                ("Password", True),
                ("Confirm Password", True),
            ]
        else:  # admin
            fields = [
                ("Full Name", False),
                ("Address", False),
                ("Phone", False),
                ("Email", False),
                ("Username", False),
                ("Password", True),
                ("Confirm Password", True),
            ]
        
        # Create fields
        for label_text, is_password in fields:
            # Label
            tk.Label(
                self.dynamic_fields_frame,
                text=label_text,
                font=("Segoe UI", 10, "bold"),
                bg="white",
                fg="#4a5568",
                anchor="w"
            ).pack(fill="x", pady=(8, 3), padx=5)

            # Entry
            entry = tk.Entry(
                self.dynamic_fields_frame,
                font=("Segoe UI", 10),
                relief="solid",
                bd=1,
                highlightthickness=2,
                highlightcolor="#764ba2",
                highlightbackground="#e2e8f0",
                show="●" if is_password else ""
            )
            entry.pack(fill="x", ipady=6, padx=5)
            self.entries[f"{label_text}:"] = entry

    def _load_side_image(self):
        """Load and display side image"""
        try:
            img = Image.open("assets/register_image.jpg")
            height = self.right_frame.winfo_height() or 550
            img = img.resize((320, height), Image.LANCZOS)
            self.side_image = ImageTk.PhotoImage(img)
            img_label = tk.Label(self.right_frame, image=self.side_image, bg="#764ba2")
            img_label.place(x=0, y=0, relwidth=1, relheight=1)
        except:
            pass

    def handle_register(self):
        user_type = self.user_type_var.get()
        full_name = self.entries.get("Full Name:", tk.Entry()).get().strip()
        address = self.entries.get("Address:", tk.Entry()).get().strip()
        phone = self.entries.get("Phone:", tk.Entry()).get().strip()
        email = self.entries.get("Email:", tk.Entry()).get().strip()
        username = self.entries.get("Username:", tk.Entry()).get().strip()
        password = self.entries.get("Password:", tk.Entry()).get().strip()
        confirm_password = self.entries.get("Confirm Password:", tk.Entry()).get().strip()

        # Validate common fields
        if not all([user_type, full_name, address, phone, email, username, password, confirm_password]):
            messagebox.showerror("Error", "All fields are required.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        user_service = self.controller.context.user_service

        try:
            # Register based on user type
            if user_type == "customer":
                user_id = user_service.register_customer(
                    full_name=full_name,
                    address=address,
                    phone=phone,
                    email=email,
                    username=username,
                    password=password,
                )
            elif user_type == "driver":
                # Get driver-specific fields
                license_number = self.entries.get("License Number:", tk.Entry()).get().strip()
                vehicle_number = self.entries.get("Vehicle Number:", tk.Entry()).get().strip()
                
                if not license_number or not vehicle_number:
                    messagebox.showerror("Error", "License Number and Vehicle Number are required for drivers.")
                    return
                
                user_id = user_service.register_driver(
                    full_name=full_name,
                    address=address,
                    phone=phone,
                    email=email,
                    license_number=license_number,
                    vehicle_number=vehicle_number,
                    username=username,
                    password=password,
                )
            elif user_type == "admin":
                user_id = user_service.register_admin(
                    full_name=full_name,
                    address=address,
                    phone=phone,
                    email=email,
                    username=username,
                    password=password,
                )
            
            messagebox.showinfo(
                "Success",
                f"Registration successful as {user_type}. You can now log in.\n(Your user id: {user_id})",
            )
            self.controller.show_frame("LoginPage")
        except ValueError as e:
            messagebox.showerror("Registration Error", str(e))
        except AttributeError as e:
            messagebox.showerror("Error", f"Registration method for {user_type} not implemented: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")