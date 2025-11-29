# run_gui.py

from ui.app_context import AppContext
from ui.main_app import MainApp


if __name__ == "__main__":
    context = AppContext()
    app = MainApp(context)
    app.mainloop()
