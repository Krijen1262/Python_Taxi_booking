# main.py
# GUI entry point for the Taxi Booking System (Tkinter + MySQL + OOP)

from ui.app_context import AppContext
from ui.main_app import MainApp


def main():
    # Create shared context (Database + Services)
    context = AppContext()

    # Create and run the Tkinter main application
    app = MainApp(context)
    app.mainloop()


if __name__ == "__main__":
    main()
