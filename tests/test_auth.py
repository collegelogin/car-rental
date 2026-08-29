import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.auth_service import AuthService
from services.db_service import DatabaseService

class TestAuthServiceDebug(unittest.TestCase):
   
    def setUp(self):
        self.auth_service = AuthService()
        self.db = DatabaseService()
        self.db.db_path = 'test_car_rental.db'
        self.db.setup_database()
   
    def tearDown(self):
        import time
        self.db.close_connection()
        time.sleep(0.5)
        if os.path.exists('test_car_rental.db'):
            try:
                os.remove('test_car_rental.db')
            except PermissionError:
                pass
   
    def test_register_valid_user_debug(self):
        print("\n"+ "="*50)
        print("DEBUG: Testing user registration")
        print("="*50)
       
        # Test data
        username = 'testuser'
        password = 'password123'
        full_name = 'Test User'
        email = 'test@example.com'
        phone = '1234567890'
        role = 'customer'
       
        print(f"Attempting to register:")
        print(f"Username: {username}")
        print(f"Password: {password}")
        print(f"Full Name: {full_name}")
        print(f"Email: {email}")
        print(f"Phone: {phone}")
        print(f"Role: {role}")
       
        # Try registration
        success, message = self.auth_service.register_user(
            username, password, full_name, email, phone, role
        )
       
        print(f"\nResult:")
        print(f"Success: {success}")
        print(f"Message: {message}")
       
        # Check if user was actually created
        if success:
            user, _ = self.auth_service.login_user(username, password)
            print(f"User created: {user is not None}")
            if user:
                print(f"User ID: {user.user_id}")
                print(f"User Role: {user.role}")
        else:
            print("Registration failed - checking database...")
            # Check what's in the database
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user_data = cursor.fetchone()
            if user_data:
                print(f"  User found in DB: {dict(user_data)}")
            else:
                print("  No user found in DB")
           
            # Check if email exists
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            email_data = cursor.fetchone()
            if email_data:
                print(f"Email found in DB: {dict(email_data)}")
       
        self.assertTrue(success, f"Registration failed: {message}")

if __name__ == '__main__':
    unittest.main(verbosity=2)
