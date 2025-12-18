from ui.app_context import AppContext
from ui.main_app import MainApp


def main():
    context = AppContext()
    app = MainApp(context)
    app.mainloop()


if __name__ == "__main__":
    main()
