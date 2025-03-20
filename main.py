from app import App
from states.main_menu import MainMenu

if __name__ == "__main__":
    app = App()
    app.state_manager.change_state(MainMenu(app))
    app.run()
