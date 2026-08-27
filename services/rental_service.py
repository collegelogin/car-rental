from datetime import datetime, timedelta
from models.car import Car
from models.booking import Booking
from services.db_service import DatabaseService

class RentalService:
    def __init__(self):
        self.db = DatabaseService()
    
    def add_car(self, make, model, year, mileage, available_now,
                min_rent_period, max_rent_period, daily_rate, late_fee_per_day):
        """Add a new car"""
        # Validate inputs
        if not make or not model:
            return False, "Make and model cannot be empty"
        
        if year < 1900 or year > datetime.now().year + 1:
            return False, "Invalid year"
        
        if mileage < 0:
            return False, "Mileage cannot be negative"
        
        if available_now not in ['yes', 'no']:
            return False, "Availability must be 'yes' or 'no'"
        
        if min_rent_period < 1:
            return False, "Minimum rent period must be at least 1 day"
        
        if max_rent_period < min_rent_period:
            return False, "Maximum rent period must be greater than minimum"
        
        if daily_rate <= 0:
            return False, "Daily rate must be positive"
        
        if late_fee_per_day < 0:
            return False, "Late fee cannot be negative"
        
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            self.db.execute_query('''
                INSERT INTO cars (make, model, year, mileage, available_now, 
                                min_rent_period, max_rent_period, daily_rate, 
                                late_fee_per_day, created_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (make, model, year, mileage, available_now, 
                  min_rent_period, max_rent_period, daily_rate, 
                  late_fee_per_day, current_date))
            
            car_id = self.db.get_last_row_id()
            return True, f"Car added successfully with ID: {car_id}"
        except Exception as e:
            return False, f"Failed to add car: {str(e)}"
    
    def get_all_cars(self):
        """Get all cars"""
        rows = self.db.fetch_all('''
            SELECT * FROM cars ORDER BY car_id
        ''')
        return [Car.from_db_row(tuple(row)) for row in rows]
    
    def get_available_cars(self):
        """Get all available cars"""
        rows = self.db.fetch_all('''
            SELECT * FROM cars WHERE available_now = 'yes' ORDER BY car_id
        ''')
        return [Car.from_db_row(tuple(row)) for row in rows]
    
    def get_car_by_id(self, car_id):
        """Get car by ID"""
        row = self.db.fetch_one(
            "SELECT * FROM cars WHERE car_id = ?", 
            (car_id,)
        )
        if row:
            return Car.from_db_row(tuple(row))
        return None
    
    def update_car(self, car_id, **kwargs):
        """Update car details"""
        # Check if car exists
        car = self.get_car_by_id(car_id)
        if not car:
            return False, "Car not found"
        
        # Build update query
        fields = []
        values = []
        
        valid_fields = ['make', 'model', 'year', 'mileage', 'available_now',
                       'min_rent_period', 'max_rent_period', 'daily_rate', 
                       'late_fee_per_day']
        
        for key, value in kwargs.items():
            if key in valid_fields and value is not None:
                fields.append(f"{key} = ?")
                values.append(value)
        
        if not fields:
            return False, "No fields to update"
        
        values.append(car_id)
        query = f"UPDATE cars SET {', '.join(fields)} WHERE car_id = ?"
        
        try:
            self.db.execute_query(query, values)
            return True, "Car updated successfully"
        except Exception as e:
            return False, f"Failed to update car: {str(e)}"
    
    def delete_car(self, car_id):
        """Delete a car"""
        # Check if car has bookings
        bookings = self.db.fetch_one(
            "SELECT COUNT(*) FROM bookings WHERE car_id = ?", 
            (car_id,)
        )
        
        if bookings and bookings[0] > 0:
            return False, f"Cannot delete car with {bookings[0]} booking(s)"
        
        try:
            self.db.execute_query("DELETE FROM cars WHERE car_id = ?", (car_id,))
            return True, "Car deleted successfully"
        except Exception as e:
            return False, f"Failed to delete car: {str(e)}"
    
    def create_booking(self, customer_id, car_id, start_date_str, end_date_str):
        """Create a new booking"""
        # Get car details
        car = self.get_car_by_id(car_id)
        if not car:
            return False, "Car not found"
        
        if not car.is_available():
            return False, "Car is not available"
        
        # Parse dates
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            return False, "Invalid date format. Use YYYY-MM-DD"
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if start_date < today:
            return False, "Cannot book a car for a past date"
        
        if end_date <= start_date:
            return False, "End date must be after start date"
        
        total_days = (end_date - start_date).days
        if total_days < 1:
            return False, "Booking must be for at least 1 day"
        
        if total_days < car.min_rent_period:
            return False, f"Minimum rent period is {car.min_rent_period} days"
        
        if total_days > car.max_rent_period:
            return False, f"Maximum rent period is {car.max_rent_period} days"
        
        # Calculate total fee
        total_fee = total_days * car.daily_rate
        
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        booking_date = datetime.now().strftime('%Y-%m-%d')
        
        try:
            self.db.execute_query('''
                INSERT INTO bookings (
                    car_id, customer_id, booking_date, rental_start_date, 
                    rental_end_date, total_days, daily_rate, total_fee, 
                    status, admin_notes, created_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (car_id, customer_id, booking_date, start_date_str, 
                  end_date_str, total_days, car.daily_rate, total_fee, 
                  'pending', '', current_date))
            
            # Mark car as unavailable
            self.db.execute_query(
                "UPDATE cars SET available_now = 'no' WHERE car_id = ?", 
                (car_id,)
            )
            
            booking_id = self.db.get_last_row_id()
            return True, f"Booking created successfully with ID: {booking_id}"
        except Exception as e:
            return False, f"Booking failed: {str(e)}"
    
    def get_customer_bookings(self, customer_id):
        """Get all bookings for a customer"""
        rows = self.db.fetch_all('''
            SELECT b.*, c.make, c.model, c.year 
            FROM bookings b
            JOIN cars c ON b.car_id = c.car_id
            WHERE b.customer_id = ?
            ORDER BY b.booking_id DESC
        ''', (customer_id,))
        return rows
    
    def get_pending_bookings(self):
        """Get all pending bookings"""
        rows = self.db.fetch_all('''
            SELECT b.*, u.full_name, c.make, c.model, c.year 
            FROM bookings b
            JOIN users u ON b.customer_id = u.user_id
            JOIN cars c ON b.car_id = c.car_id
            WHERE b.status = 'pending'
            ORDER BY b.booking_date
        ''')
        return rows
    
    def get_all_bookings(self):
        """Get all bookings"""
        rows = self.db.fetch_all('''
            SELECT b.*, u.full_name, c.make, c.model, c.year 
            FROM bookings b
            JOIN users u ON b.customer_id = u.user_id
            JOIN cars c ON b.car_id = c.car_id
            ORDER BY b.booking_id DESC
        ''')
        return rows
    
    def approve_booking(self, booking_id, admin_notes=''):
        """Approve a booking"""
        booking = self.db.fetch_one(
        "SELECT car_id FROM bookings WHERE booking_id = ?", 
        (booking_id,)
        )
    
        if not booking:
            return False, "Booking not found"
        try:
            self.db.execute_query('''
                UPDATE bookings 
                SET status = 'approved', admin_notes = ?
                WHERE booking_id = ?
                ''', (admin_notes, booking_id))
        
            self.db.execute_query(
                "UPDATE cars SET available_now = 'no' WHERE car_id = ?", 
                (booking['car_id'],)
                )
            return True, "Booking approved successfully"
        except Exception as e:
            return False, f"Failed to approve booking: {str(e)}"
    
    def reject_booking(self, booking_id, admin_notes):
        """Reject a booking and make car available"""
        if not admin_notes:
            return False, "Rejection reason is required"
        
        # Get booking details
        booking = self.db.fetch_one(
            "SELECT car_id FROM bookings WHERE booking_id = ?", 
            (booking_id,)
        )
        
        if not booking:
            return False, "Booking not found"
        
        try:
            # Update booking status
            self.db.execute_query('''
                UPDATE bookings 
                SET status = 'rejected', admin_notes = ?
                WHERE booking_id = ?
            ''', (admin_notes, booking_id))
            
            # Make car available again
            self.db.execute_query(
                "UPDATE cars SET available_now = 'yes' WHERE car_id = ?", 
                (booking['car_id'],)
            )
            
            return True, "Booking rejected successfully"
        except Exception as e:
            return False, f"Failed to reject booking: {str(e)}"

    def complete_booking(self, booking_id, actual_return_date_str=None):
        """Complete a booking and calculate any late fees"""
        from datetime import datetime, timedelta
        
        # Get booking details
        booking = self.db.fetch_one(
            "SELECT * FROM bookings WHERE booking_id = ?", 
            (booking_id,)
        )
        
        if not booking:
            return False, "Booking not found"
        
        if booking['status'] != 'approved':
            return False, "Booking must be approved before completing"
        
        # Get car details for late fee
        car = self.get_car_by_id(booking['car_id'])
        if not car:
            return False, "Car not found"
        
        # Determine actual return date
        if actual_return_date_str:
            try:
                actual_return = datetime.strptime(actual_return_date_str, '%Y-%m-%d')
            except ValueError:
                return False, "Invalid date format. Use YYYY-MM-DD"
        else:
            actual_return = datetime.now()
        
        # Parse rental end date
        rental_end = datetime.strptime(booking['rental_end_date'], '%Y-%m-%d')
        
        # Calculate late fee if applicable
        late_fee = 0
        if actual_return > rental_end:
            days_late = (actual_return - rental_end).days
            late_fee = days_late * car.late_fee_per_day
        
        try:
            # Update booking status
            self.db.execute_query('''
                UPDATE bookings 
                SET status = 'completed', admin_notes = ?
                WHERE booking_id = ?
            ''', (f"Returned on {actual_return.strftime('%Y-%m-%d')}. Late fee: ${late_fee:.2f}", booking_id))
            
            # Make car available again
            self.db.execute_query(
                "UPDATE cars SET available_now = 'yes' WHERE car_id = ?", 
                (booking['car_id'],)
            )
            message = f"Booking completed successfully"
            if late_fee > 0:
                message += f". Late fee of ${late_fee:.2f} applied for {days_late} day(s) late."
            
            return True, message
        except Exception as e:
            return False, f"Failed to complete booking: {str(e)}"
