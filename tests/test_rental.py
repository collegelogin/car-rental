import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.rental_service import RentalService
from services.auth_service import AuthService
from services.db_service import DatabaseService

class TestRentalServiceDebug(unittest.TestCase):
        #Test rental service with debugging
   
    def setUp(self):
        #Set up test environment
        # Use a unique test database name with timestamp
        import time
        self.test_db_path = f'test_car_rental_{int(time.time())}.db'
       
        # Initialize database service
        self.db = DatabaseService(self.test_db_path)
        self.db.setup_database()
       
        # Create auth service
        self.auth_service = AuthService()
        self.auth_service.db = self.db
       
        # Create rental service
        self.rental_service = RentalService()
        self.rental_service.db = self.db
       
        # Create a test user
        self.auth_service.register_user(
            'testuser', 'password123', 'Test User',
            'test@example.com', '1234567890', 'customer'
        )
        self.user, _ = self.auth_service.login_user('testuser', 'password123')
       
        print(f"\nTest database: {self.test_db_path}")
   
    def tearDown(self):
        
        import time
        self.db.close_connection()
        time.sleep(0.5)
        if os.path.exists(self.test_db_path):
            try:
                os.remove(self.test_db_path)
                print(f"Removed test database: {self.test_db_path}")
            except PermissionError:
                print(f"Could not remove test database: {self.test_db_path}")
   
    def test_add_car(self):
        print("\n Test: Adding a car...")
       
        success, message = self.rental_service.add_car(
            'Toyota', 'Camry', 2020, 10000, 'yes',
            2, 7, 50.0, 25.0
        )
       
        self.assertTrue(success)
        self.assertIn("Car added successfully", message)
       
        # Verify car was added
        cars = self.rental_service.get_all_cars()
        print(f"  Cars in database: {len(cars)}")
        self.assertEqual(len(cars), 1)
   
    def test_get_available_cars(self):
        print("\nTest: Getting available cars...")
       
        # First, check current state
        print("Checking current database state...")
        all_cars = self.rental_service.get_all_cars()
        print(f"Total cars in database: {len(all_cars)}")
       
        # Add a car
        print("Adding a car...")
        self.rental_service.add_car(
            'Toyota', 'Camry', 2020, 10000, 'yes',
            2, 7, 50.0, 25.0
        )
       
        # Check after adding
        all_cars = self.rental_service.get_all_cars()
        print(f"Total cars after add: {len(all_cars)}")
       
        for car in all_cars:
            print(f"Car: {car.make} {car.model} - Available: {car.available_now}")
       
        # Get available cars
        available_cars = self.rental_service.get_available_cars()
        print(f"Available cars: {len(available_cars)}")
       
        for car in available_cars:
            print(f"Available Car: {car.make} {car.model}")
       
        # This should be 1
        self.assertEqual(len(available_cars), 1,
                         f"Expected 1 available car, but found {len(available_cars)}")
       
        # Verify the car is the one we added
        if available_cars:
            self.assertEqual(available_cars[0].make, 'Toyota')
            self.assertEqual(available_cars[0].model, 'Camry')
   
    def test_create_booking(self):
        print("\nTest: Creating a booking...")
       
        # Add a car
        self.rental_service.add_car(
            'Toyota', 'Camry', 2020, 10000, 'yes',
            2, 7, 50.0, 25.0
        )
       
        # Get available cars
        cars = self.rental_service.get_available_cars()
        self.assertTrue(len(cars) > 0, "No cars available for booking test")
       
        car = cars[0]
        print(f"Booking car: {car.make} {car.model}")
       
        success, message = self.rental_service.create_booking(
            self.user.user_id, car.car_id, '2024-12-01', '2024-12-05'
        )
        self.assertTrue(success)
        self.assertIn("Booking created successfully", message)
       
        # Verify booking was created
        bookings = self.rental_service.get_customer_bookings(self.user.user_id)
        print(f"Bookings created: {len(bookings)}")
        self.assertEqual(len(bookings), 1)

if __name__ == '__main__':
    unittest.main(verbosity=2)
