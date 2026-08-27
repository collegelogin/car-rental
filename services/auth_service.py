import re
from datetime import datetime
from models.user import User
from services.db_service import DatabaseService
from utils.security import SecurityUtils
from utils.validators import Validators

class AuthService:
    #handling user authentication
    
    def __init__(self):
        self.db = DatabaseService()
    
    def register_user(self, username, password, full_name, email, phone, role):
        #registering new user
        # Validate inputs
        if not username:
            return False, "Username cannot be empty"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        if not full_name:
            return False, "Full name cannot be empty"
        
        if not Validators.validate_email(email):
            return False, "Invalid email format"
        
        if not phone:
            return False, "Phone number cannot be empty"

        if not Validators.validate_phone(phone):
            return False, "Invalid phone number format"
        
        if role not in ['customer', 'admin']:
            return False, "Role must be 'customer' or 'admin'"
        
        # Check if username exists
        existing_user = self.db.fetch_one(
            "SELECT username FROM users WHERE username = ?", 
            (username,)
        )
        if existing_user:
            return False, "Username already taken"
        
        # Check if email exists
        existing_email = self.db.fetch_one(
            "SELECT email FROM users WHERE email = ?", 
            (email,)
        )
        if existing_email:
            return False, "Email already registered"
        
        # Hash password and save
        hashed_password = SecurityUtils.hash_password(password)
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            self.db.execute_query('''
                INSERT INTO users (username, password, full_name, email, phone, role, created_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (username, hashed_password, full_name, email, phone, role, current_date))
            
            return True, "Registration successful"
        except Exception as e:
            return False, f"Registration failed: {str(e)}"
    
    def login_user(self, username, password):
        """Login an existing user"""
        if not username or not password:
            return None, "Username and password cannot be empty"
        
        user_data = self.db.fetch_one(
            "SELECT * FROM users WHERE username = ?", 
            (username,)
        )
        
        if not user_data:
            return None, "Invalid username or password"
        
        if user_data['password'] != SecurityUtils.hash_password(password):
            return None, "Invalid username or password"
        
        user = User.from_db_row(tuple(user_data))
        return user, "Login successful"
    
    def get_user_by_id(self, user_id):
        #get user by id
        user_data = self.db.fetch_one(
            "SELECT * FROM users WHERE user_id = ?", 
            (user_id,)
        )
        
        if not user_data:
            return None
        
        return User.from_db_row(tuple(user_data))

    def change_password(self, user_id, old_password, new_password):
        # Get user
        user = self.get_user_by_id(user_id)
        if not user:
            return False, "User not found"
    
        # Verify old password
        if user.password != SecurityUtils.hash_password(old_password):
            return False, "Current password is incorrect"
    
        # Validate new password
        if len(new_password) < 6:
            return False, "New password must be at least 6 characters"
    
        # Update password
        try:
            hashed_password = SecurityUtils.hash_password(new_password)
            self.db.execute_query(
                "UPDATE users SET password = ? WHERE user_id = ?",
                (hashed_password, user_id)
                )
            return True, "Password changed successfully"
        except Exception as e:
            return False, f"Failed to change password: {str(e)}"
