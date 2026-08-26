from ui.main_menu import MainMenu
from services.db_service import DatabaseService

def main():
    # Initialize database
    db = DatabaseService()
    db.setup_database()
    db.create_default_admin()
    
    print("\n System ready!")
    
    # Start main menu
    menu = MainMenu()
    menu.display()

if __name__ == "__main__":
    main()
