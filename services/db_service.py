import sqlite3
from datetime import datetime
from utils.security import SecurityUtils

class DatabaseService:
    def __init__(self, db_path='car_rental.db'):
        self.db_path = db_path
        self.connection = None
    
    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def setup_database(self):
        #creating necessary tables
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'customer')),
                created_date TEXT NOT NULL
            )
        ''')
        
        # Create Cars table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                car_id INTEGER PRIMARY KEY AUTOINCREMENT,
                model TEXT NOT NULL,
                year INTEGER NOT NULL,
                mileage INTEGER NOT NULL,
                available_now TEXT NOT NULL CHECK(available_now IN ('yes', 'no')),
                min_rent_period INTEGER NOT NULL,
                max_rent_period INTEGER NOT NULL,
                daily_rate REAL NOT NULL,
                late_fee_per_day REAL NOT NULL,
                created_date TEXT NOT NULL
            )
        ''')
        
        # Create Bookings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                car_id INTEGER NOT NULL,
                customer_id INTEGER NOT NULL,
                booking_date TEXT NOT NULL,
                rental_start_date TEXT NOT NULL,
                rental_end_date TEXT NOT NULL,
                total_days INTEGER NOT NULL,
                daily_rate REAL NOT NULL,
                total_fee REAL NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('pending', 'approved', 'rejected', 'completed')),
                admin_notes TEXT,
                created_date TEXT NOT NULL,
                FOREIGN KEY (car_id) REFERENCES cars(car_id),
                FOREIGN KEY (customer_id) REFERENCES users(user_id)
            )
        ''')
        
        conn.commit()
    
    def create_default_admin(self):
        #create admin account
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if any admin exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
        admin_count = cursor.fetchone()[0]
        
        if admin_count == 0:
            # Create default admin
            hashed_password = SecurityUtils.hash_password('admin123')
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cursor.execute('''
                INSERT INTO users (username, password, full_name, email, phone, role, created_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', ('admin', hashed_password, 'System Administrator', 
                  'sandhya@carrental.com', '1234567890', 'admin', current_date))
            
            conn.commit()
            print("\n Default admin created!")
            print("   Username: admin")
            print("   Password: admin123")
    
    def execute_query(self, query, params=None):
        #execute a query
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        conn.commit()
        return cursor
    
    def fetch_all(self, query, params=None):
        #fetching result from a query
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        return cursor.fetchall()
    
    def fetch_one(self, query, params=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchone()
    
    def get_last_row_id(self):
        #get insert row id
        conn = self.get_connection()
        return conn.execute("SELECT last_insert_rowid()").fetchone()[0]
