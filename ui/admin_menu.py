from services.rental_service import RentalService
from services.auth_service import AuthService  
class AdminMenu:
    
    def __init__(self, user):
        self.user = user
        self.rental_service = RentalService()
        self.auth_service = AuthService()  
    
    def display(self):
        while True:
            print("\n" + "="*50)
            print(f"WELCOME, {self.user.full_name.upper()}")
            print("ADMIN MENU")
            print("="*50)
            print("1. View All Cars")
            print("2. Add New Car")
            print("3. Update Car")
            print("4. Delete Car")
            print("5. Manage Bookings (Approve/Reject/Complete)")
            print("6. View All Bookings")
            print("7. Change Password")  
            print("8. Logout")
            print("="*50)
            
            choice = input("Enter your choice (1-8): ").strip()
            
            if choice == '1':
                self.view_all_cars()
            elif choice == '2':
                self.add_car()
            elif choice == '3':
                self.update_car()
            elif choice == '4':
                self.delete_car()
            elif choice == '5':
                self.manage_bookings()
            elif choice == '6':
                self.view_all_bookings()
            elif choice == '7': 
                self.change_password()
            elif choice == '8':
                print(f"\nGoodbye, {self.user.full_name}!")
                break
            else:
                print("Invalid choice! Please try again.")
    
    def view_all_cars(self):
        """View all cars"""
        print("\n" + "="*50)
        print("ALL CARS IN SYSTEM")
        print("="*50)
        
        cars = self.rental_service.get_all_cars()
        
        if not cars:
            print("\nNo cars found in the system!")
            return
        
        print(f"\n{'ID':<5} {'Make':<12} {'Model':<12} {'Year':<6} {'Mileage':<10} {'Available':<10} {'Min Days':<8} {'Max Days':<8} {'Rate($)':<8} {'Late Fee($)':<10}")
        print("-" * 100)
        
        for car in cars:
            print(f"{car.car_id:<5} {car.make:<12} {car.model:<12} {car.year:<6} {car.mileage:<10} {car.available_now:<10} {car.min_rent_period:<8} {car.max_rent_period:<8} {car.daily_rate:<8.2f} {car.late_fee_per_day:<10.2f}")
        
        print("\n" + "="*50)
    
    def add_car(self):
        """Add a new car"""
        print("\n" + "="*50)
        print("            ADD NEW CAR")
        print("="*50)
        
        make = input("Enter car make (e.g., Toyota): ").strip()
        if not make:
            print("Car make cannot be empty!")
            return
        
        model = input("Enter car model (e.g., Camry): ").strip()
        if not model:
            print("Car model cannot be empty!")
            return
        
        try:
            year = int(input("Enter year (e.g., 2020): ").strip())
        except ValueError:
            print("Please enter a valid number for year!")
            return
        
        try:
            mileage = int(input("Enter mileage (km): ").strip())
        except ValueError:
            print("Please enter a valid number for mileage!")
            return
        
        available_now = input("Is car available now? (yes/no): ").strip().lower()
        if available_now not in ['yes', 'no']:
            print("Please enter 'yes' or 'no'!")
            return
        
        try:
            min_rent_period = int(input("Enter minimum rent period (days): ").strip())
        except ValueError:
            print("Please enter a valid number for minimum rent period!")
            return
        
        try:
            max_rent_period = int(input("Enter maximum rent period (days): ").strip())
        except ValueError:
            print("Please enter a valid number for maximum rent period!")
            return
        
        try:
            daily_rate = float(input("Enter daily rate ($): ").strip())
        except ValueError:
            print("Please enter a valid number for daily rate!")
            return
        
        try:
            late_fee_per_day = float(input("Enter late fee per day ($): ").strip())
        except ValueError:
            print("Please enter a valid number for late fee!")
            return
        
        success, message = self.rental_service.add_car(
            make, model, year, mileage, available_now,
            min_rent_period, max_rent_period, daily_rate, late_fee_per_day
        )
        
        if success:
            print(f"\n{message}")
        else:
            print(f"\n{message}")
    
    def update_car(self):
        """Update an existing car"""
        print("\n" + "="*50)
        print("         UPDATE CAR DETAILS")
        print("="*50)
        
        self.view_all_cars()
        
        try:
            car_id = int(input("\nEnter Car ID to update: ").strip())
        except ValueError:
            print("Invalid Car ID!")
            return
        
        car = self.rental_service.get_car_by_id(car_id)
        if not car:
            print(f"Car with ID {car_id} not found!")
            return
        
        print(f"\nUpdating car: {car.get_full_name()}")
        print("Leave blank to keep current value")
        
        make = input(f"Make [{car.make}]: ").strip() or car.make
        model = input(f"Model [{car.model}]: ").strip() or car.model
        
        year_input = input(f"Year [{car.year}]: ").strip()
        year = int(year_input) if year_input else car.year
        
        mileage_input = input(f"Mileage [{car.mileage}]: ").strip()
        mileage = int(mileage_input) if mileage_input else car.mileage
        
        available = input(f"Available now (yes/no) [{car.available_now}]: ").strip().lower()
        available = available if available else car.available_now
        
        min_rent_input = input(f"Min rent period (days) [{car.min_rent_period}]: ").strip()
        min_rent = int(min_rent_input) if min_rent_input else car.min_rent_period
        
        max_rent_input = input(f"Max rent period (days) [{car.max_rent_period}]: ").strip()
        max_rent = int(max_rent_input) if max_rent_input else car.max_rent_period
        
        rate_input = input(f"Daily rate ($) [{car.daily_rate}]: ").strip()
        daily_rate = float(rate_input) if rate_input else car.daily_rate
        
        late_fee_input = input(f"Late fee per day ($) [{car.late_fee_per_day}]: ").strip()
        late_fee = float(late_fee_input) if late_fee_input else car.late_fee_per_day
        
        success, message = self.rental_service.update_car(
            car_id,
            make=make, model=model, year=year, mileage=mileage,
            available_now=available, min_rent_period=min_rent,
            max_rent_period=max_rent, daily_rate=daily_rate,
            late_fee_per_day=late_fee
        )
        
        if success:
            print(f"\n{message}")
        else:
            print(f"\n{message}")
    
    def delete_car(self):
        """Delete a car"""
        print("\n" + "="*50)
        print("DELETE CAR")
        print("="*50)
        
        self.view_all_cars()
        
        try:
            car_id = int(input("\nEnter Car ID to delete: ").strip())
        except ValueError:
            print("Invalid Car ID!")
            return
        
        confirm = input(f"Are you sure you want to delete car ID {car_id}? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Deletion cancelled.")
            return
        
        success, message = self.rental_service.delete_car(car_id)
        
        if success:
            print(f"\n{message}")
        else:
            print(f"\n{message}")
    
    def manage_bookings(self):
        """Manage bookings - FIXED with status checking"""
        print("\n" + "="*50)
        print("        MANAGE BOOKINGS")
        print("="*50)
        
        # 1. Show pending bookings
        pending = self.rental_service.get_pending_bookings()
        
        if pending:
            print("\nPENDING BOOKINGS:")
            print(f"{'ID':<6} {'Customer':<20} {'Car':<20} {'Start':<14} {'End':<14} {'Days':<6} {'Fee($)':<10}")
            print("-" * 95)
            
            for booking in pending:
                car_info = f"{booking['make']} {booking['model']} ({booking['year']})"
                print(f"{booking['booking_id']:<6} {booking['full_name']:<20} {car_info:<20} {booking['rental_start_date']:<14} {booking['rental_end_date']:<14} {booking['total_days']:<6} {booking['total_fee']:<10.2f}")
        else:
            print("\nNo pending bookings to manage!")
        
        # 2. Show approved bookings (for completion)
        approved = self.rental_service.db.fetch_all('''
            SELECT b.booking_id, u.full_name, c.make, c.model, c.year,
                b.rental_start_date, b.rental_end_date,
                b.total_days, b.total_fee
            FROM bookings b
            JOIN users u ON b.customer_id = u.user_id
            JOIN cars c ON b.car_id = c.car_id
            WHERE b.status = 'approved'
            ORDER BY b.booking_date
        ''')
        
        if approved:
            print("\nAPPROVED BOOKINGS (Ready to complete):")
            print(f"{'ID':<6} {'Customer':<20} {'Car':<20} {'Start':<14} {'End':<14} {'Days':<6} {'Fee($)':<10}")
            print("-" * 95)
        
        for booking in approved:
            car_info = f"{booking['make']} {booking['model']} ({booking['year']})"
            print(f"{booking['booking_id']:<6} {booking['full_name']:<20} {car_info:<20} {booking['rental_start_date']:<14} {booking['rental_end_date']:<14} {booking['total_days']:<6} {booking['total_fee']:<10.2f}")
        
        print("\nOptions:")
        print("1. Approve a pending booking")
        print("2. Reject a pending booking")
        print("3. Complete a booking (mark as returned)")  
        print("4. Cancel")  
        
        choice = input("Choose action (1-4): ").strip()
        
        if choice == '1':
            if not pending:
                print("No pending bookings to approve!")
                return
            
            try:
                booking_id = int(input("Enter Booking ID to approve: ").strip())
            except ValueError:
                print("Invalid Booking ID!")
                return
            
            booking_check = self.rental_service.db.fetch_one(
                "SELECT status FROM bookings WHERE booking_id = ?",
                (booking_id,)
            )
            
            if not booking_check:
                print("Booking not found!")
                return
            
            if booking_check['status'] != 'pending':
                print(f"Booking is already {booking_check['status']}!")
                return
            
            notes = input("Enter admin notes (optional): ").strip()
            success, message = self.rental_service.approve_booking(booking_id, notes)
            print(f"\n {message}" if success else f"\n {message}")

        elif choice == '2':
            if not pending:
                print("No pending bookings to reject!")
                return
            
            try:
                booking_id = int(input("Enter Booking ID to reject: ").strip())
            except ValueError:
                print("Invalid Booking ID!")
                return
            
            booking_check = self.rental_service.db.fetch_one(
                "SELECT status FROM bookings WHERE booking_id = ?",
                (booking_id,)
            )
            
            if not booking_check:
                print("Booking not found!")
                return
            
            if booking_check['status'] != 'pending':
                print(f"Booking is already {booking_check['status']}!")
                return
            
            notes = input("Enter rejection reason: ").strip()
            if not notes:
                print("Rejection reason is required!")
                return
            
            success, message = self.rental_service.reject_booking(booking_id, notes)
            print(f"\n{message}" if success else f"\n {message}")
        
        elif choice == '3':  
            if not approved:
                print("No approved bookings to complete!")
                return
            
            try:
                booking_id = int(input("Enter Booking ID to complete: ").strip())
            except ValueError:
                print("Invalid Booking ID!")
                return
            
            booking_check = self.rental_service.db.fetch_one(
                "SELECT status FROM bookings WHERE booking_id = ?",
                (booking_id,)
            )
            
            if not booking_check:
                print("Booking not found!")
                return
            
            if booking_check['status'] != 'approved':
                print(f"Booking is {booking_check['status']}, not 'approved'!")
                return
            
            actual_return = input("Enter actual return date (YYYY-MM-DD) [press Enter for today]: ").strip()
            if not actual_return:
                actual_return = None
            
            success, message = self.rental_service.complete_booking(booking_id, actual_return)
            print(f"\n{message}" if success else f"\n {message}")
        
        elif choice == '4': 
            print("Operation cancelled.")
        
        else:
            print("Invalid choice!")
    
    def view_all_bookings(self):
        """View all bookings"""
        print("\n" + "="*50)
        print("ALL BOOKINGS")
        print("="*50)
        
        bookings = self.rental_service.get_all_bookings()
        
        if not bookings:
            print("\n No bookings found!")
            return
        
        print(f"\n{'ID':<6} {'Customer':<18} {'Car':<18} {'Start':<12} {'End':<12} {'Days':<6} {'Fee($)':<8} {'Status':<10} {'Notes':<15}")
        print("-" * 120)
        
        for booking in bookings:
            car_info = f"{booking['make']} {booking['model']}"
            notes = booking['admin_notes'] if booking['admin_notes'] else '-'
            print(f"{booking['booking_id']:<6} {booking['full_name']:<18} {car_info:<18} {booking['rental_start_date']:<12} {booking['rental_end_date']:<12} {booking['total_days']:<6} {booking['total_fee']:<8.2f} {booking['status']:<10} {notes:<15}")
        
        print("\n" + "="*50)
    # Add to menu options
    def change_password(self):
        """Change user password"""
        print("\n" + "="*50)
        print("CHANGE PASSWORD")
        print("="*50)
        
        old_password = input("Enter current password: ").strip()
        new_password = input("Enter new password (min 6 characters): ").strip()
        confirm_password = input("Confirm new password: ").strip()
        
        if new_password != confirm_password:
            print("Passwords do not match!")
            return
        
        success, message = self.auth_service.change_password(
            self.user.user_id, old_password, new_password
        )
        
        if success:
            print(f"\n{message}")
        else:
            print(f"\n{message}")
                       