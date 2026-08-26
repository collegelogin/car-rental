from services.auth_service import AuthService
from ui.admin_menu import AdminMenu
from ui.customer_menu import CustomerMenu
class MainMenu:
    def __init__(self):
        self.auth_service = AuthService()
    
    def display(self):
        while True:
            print("\n" + "="*50)
            print(" CAR RENTAL SYSTEM")
            print("="*50)
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            print("="*50)
            
            choice = input("Enter your choice (1-3): ").strip()
            if choice == '1':
                self.register()
            elif choice == '2':
                self.login()
            elif choice == '3':
                print("\n Thank you for using Car Rental System!")
                break
            else:
                print("Invalid choice! Please try again.")
    
    def register(self):
        """Handle user registration"""
        print("\n" + "="*50)
        print("USER REGISTRATION")
        print("="*50)
        
        username = input("Enter username: ").strip()
        password = input("Enter password (min 6 characters): ").strip()
        full_name = input("Enter full name: ").strip()
        email = input("Enter email: ").strip()
        phone = input("Enter phone number: ").strip()
        
        while True:
            role = input("Enter role (customer/admin): ").strip().lower()
            if role in ['customer', 'admin']:
                break
            print(" Role must be 'customer' or 'admin'!")
        
        success, message = self.auth_service.register_user(
            username, password, full_name, email, phone, role
        )
        
        if success:
            print(f"\n {message}")
        else:
            print(f"\n {message}")
    
    def login(self):
        """Handle user login"""
        print("\n" + "="*50)
        print("USER LOGIN")
        print("="*50)
        
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        
        user, message = self.auth_service.login_user(username, password)
        
        if user:
            print(f"\n {message}")
            print(f" Welcome back, {user.full_name}!")
            print(f" Role: {user.role}")
            
            if user.role == 'customer':
                CustomerMenu(user).display()
            else:
                AdminMenu(user).display()
        else:
            print(f"\n {message}")
