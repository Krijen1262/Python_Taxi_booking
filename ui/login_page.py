# ui/login_page.py

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class LoginPage(tk.Frame):
    """
    Enhanced styled login screen with gradient background and side image.
    On success:
    - sets controller.current_user
    - navigates to CustomerDashboard / DriverDashboard / AdminDashboard
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # ===== GRADIENT BACKGROUND =====
        self.configure(bg="#667eea")
        
        # Bind to window resize to redraw gradient
        self.bind("<Configure>", self._on_resize)
        
        # Create canvas for gradient effect
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # ===== MAIN CONTAINER =====
        self.main_container = tk.Frame(self.canvas, bg="white")
        # Use place with specific dimensions that work for both normal and maximized
        self.main_container.place(relx=0.5, rely=0.5, anchor="c", width=800, height=500)

        # ===== LEFT SIDE - IMAGE SECTION =====
        self.left_frame = tk.Frame(self.main_container, bg="#667eea", width=350)
        self.left_frame.pack(side="left", fill="both", expand=False)
        self.left_frame.pack_propagate(False)

        # Try to load decorative image
        self.side_image = None
        try:
            img = Image.open("assets/login_image.jpg")
            # Will resize on window resize
            self._load_side_image()
        except Exception:
            # Fallback decorative content
            self._create_fallback_content()

        # ===== RIGHT SIDE - LOGIN FORM =====
        self.right_frame = tk.Frame(self.main_container, bg="white", width=450)
        self.right_frame.pack(side="right", fill="both", expand=False)
        self.right_frame.pack_propagate(False)
        
        # Inner padding frame
        form_container = tk.Frame(self.right_frame, bg="white")
        form_container.place(relx=0.5, rely=0.5, anchor="c")

        # ===== TITLE =====
        title = tk.Label(
            form_container,
            text="Taxi Booking System",
            font=("Segoe UI", 24, "bold"),
            bg="white",
            fg="#1a202c",
        )
        title.pack(pady=(0, 5))

        subtitle = tk.Label(
            form_container,
            text="Sign in to your account",
            font=("Segoe UI", 11),
            bg="white",
            fg="#718096",
        )
        subtitle.pack(pady=(0, 30))

        # ===== FORM =====
        form_frame = tk.Frame(form_container, bg="white")
        form_frame.pack()

        # Username field
        tk.Label(
            form_frame,
            text="Username",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#4a5568",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))

        self.username_entry = tk.Entry(
            form_frame,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1,
            width=35,
            highlightthickness=2,
            highlightcolor="#667eea",
            highlightbackground="#e2e8f0"
        )
        self.username_entry.pack(fill="x", ipady=8, pady=(0, 20))

        # Password field
        tk.Label(
            form_frame,
            text="Password",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#4a5568",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))

        self.password_entry = tk.Entry(
            form_frame,
            show="●",
            font=("Segoe UI", 11),
            relief="solid",
            bd=1,
            width=35,
            highlightthickness=2,
            highlightcolor="#667eea",
            highlightbackground="#e2e8f0"
        )
        self.password_entry.pack(fill="x", ipady=8, pady=(0, 25))

        # ===== BUTTONS =====
        login_btn = tk.Button(
            form_frame,
            text="Login",
            font=("Segoe UI", 11, "bold"),
            bg="#667eea",
            fg="white",
            activebackground="#5568d3",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.handle_login,
            bd=0,
            width=35
        )
        login_btn.pack(fill="x", ipady=10, pady=(0, 15))

        # Divider
        divider_frame = tk.Frame(form_frame, bg="white")
        divider_frame.pack(fill="x", pady=(0, 15))
        
        tk.Frame(divider_frame, bg="#e2e8f0", height=1).pack(side="left", fill="x", expand=True, padx=(0, 10))
        tk.Label(divider_frame, text="OR", font=("Segoe UI", 9), bg="white", fg="#a0aec0").pack(side="left")
        tk.Frame(divider_frame, bg="#e2e8f0", height=1).pack(side="left", fill="x", expand=True, padx=(10, 0))

        register_btn = tk.Button(
            form_frame,
            text="Register if new",
            font=("Segoe UI", 10),
            bg="#f7fafc",
            fg="#667eea",
            activebackground="#edf2f7",
            activeforeground="#5568d3",
            relief="solid",
            bd=1,
            cursor="hand2",
            width=35,
            command=lambda: self.controller.show_frame("RegisterPage"),
        )
        register_btn.pack(fill="x", ipady=8)

    def _on_resize(self, event=None):
        """Handle window resize to redraw gradient"""
        self.after(10, self._draw_gradient)
        
    def _draw_gradient(self):
        """Draw a gradient background on canvas"""
        self.canvas.delete("gradient")
        width = self.canvas.winfo_width() or 900
        height = self.canvas.winfo_height() or 600
        
        # Gradient from purple-blue to lighter blue
        step = max(1, height // 100)
        for i in range(0, height, step):
            ratio = i / height
            r = int(102 + (139 - 102) * ratio)
            g = int(126 + (161 - 126) * ratio)
            b = int(234 + (242 - 234) * ratio)
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_rectangle(0, i, width, i + step, fill=color, outline=color, tags="gradient")

    def _create_fallback_content(self):
        """Create fallback decorative content when image not found"""
        deco_frame = tk.Frame(self.left_frame, bg="#667eea")
        deco_frame.place(relx=0.5, rely=0.5, anchor="c")
        
        tk.Label(
            deco_frame,
            text="🚖",
            font=("Segoe UI", 80),
            bg="#667eea",
            fg="white"
        ).pack(pady=20)
        
        tk.Label(
            deco_frame,
            text="Welcome Back!",
            font=("Segoe UI", 20, "bold"),
            bg="#667eea",
            fg="white"
        ).pack()
        
        tk.Label(
            deco_frame,
            text="Login to continue your\njourney with us",
            font=("Segoe UI", 12),
            bg="#667eea",
            fg="white",
            justify="center"
        ).pack(pady=10)

    def _load_side_image(self):
        """Load and display side image"""
        try:
            img = Image.open("assets/login_image.jpg")
            height = self.left_frame.winfo_height() or 500
            img = img.resize((350, height), Image.LANCZOS)
            self.side_image = ImageTk.PhotoImage(img)
            img_label = tk.Label(self.left_frame, image=self.side_image, bg="#667eea")
            img_label.place(x=0, y=0, relwidth=1, relheight=1)
        except:
            pass

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

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