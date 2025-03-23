from app import App
from myapp.screens.main_menu import MainMenu

if __name__ == "__main__":
    app = App()
    app.state_manager.add_state(MainMenu(app))
    app.state_manager.set_active(0)
    app.run()
