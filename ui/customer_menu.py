from services.rental_service import RentalService

class CustomerMenu:
    def __init__(self, user):
        self.user = user
        self.rental_service = RentalService()
    
    def display(self):
        while True:
            print("\n" + "="*50)
            print(f"WELCOME, {self.user.full_name.upper()}")
            print("CUSTOMER MENU")
            print("="*50)
            print("1. View Available Cars")
            print("2. Book a Car")
            print("3. View My Bookings")
            print("4. Logout")
            print("="*50)
            
            choice = input("Enter your choice (1-4): ").strip()
            if choice == '1':
                self.view_available_cars()
            elif choice == '2':
                self.book_car()
            elif choice == '3':
                self.view_my_bookings()
            elif choice == '4':
                print(f"\n Goodbye, {self.user.full_name}!")
                break
            else:
                print(" Invalid choice! Please try again.")
    
    def view_available_cars(self):
        """View available cars"""
        print("\n" + "="*50)
        print("AVAILABLE CARS FOR RENT")
        print("="*50)
        
        cars = self.rental_service.get_available_cars()
        
        if not cars:
            print("\n No cars currently available for rent!")
            return
        
        print(f"\n{'ID':<5} {'Make':<12} {'Model':<12} {'Year':<6} {'Mileage':<10} {'Min Days':<8} {'Max Days':<8} {'Rate($)':<8} {'Late Fee($)':<10}")
        print("-" * 90)
        
        for car in cars:
            print(f"{car.car_id:<5} {car.make:<12} {car.model:<12} {car.year:<6} {car.mileage:<10} {car.min_rent_period:<8} {car.max_rent_period:<8} {car.daily_rate:<8.2f} {car.late_fee_per_day:<10.2f}")
        
        print("\n" + "="*50)
    
    def book_car(self):
        """Book a car"""
        print("\n" + "="*50)
        print("CAR BOOKING")
        print("="*50)
        
        self.view_available_cars()
        
        try:
            car_id = int(input("\nEnter Car ID to book: ").strip())
        except ValueError:
            print("Invalid Car ID!")
            return
        
        car = self.rental_service.get_car_by_id(car_id)
        if not car:
            print(f"Car ID {car_id} not found!")
            return
        
        if not car.is_available():
            print(f"Car ID {car_id} is not available!")
            return
        
        print(f"\n Selected Car: {car.get_full_name()}")
        print(f"Daily Rate: ${car.daily_rate:.2f}")
        print(f"Min Rent: {car.min_rent_period} days")
        print(f"Max Rent: {car.max_rent_period} days")
        
        start_date_str = input("\nEnter rental start date (YYYY-MM-DD): ").strip()
        end_date_str = input("Enter rental end date (YYYY-MM-DD): ").strip()
        
        success, message = self.rental_service.create_booking(
            self.user.user_id, car_id, start_date_str, end_date_str
        )
        
        if success:
            print(f"\n {message}")
        else:
            print(f"\n {message}")
    
    def view_my_bookings(self):
        """View customer's bookings"""
        print("\n" + "="*50)
        print("MY BOOKINGS")
        print("="*50)
        
        bookings = self.rental_service.get_customer_bookings(self.user.user_id)
        
        if not bookings:
            print("\n No bookings found!")
            return
        
        print(f"\n{'ID':<6} {'Car':<20} {'Start Date':<14} {'End Date':<14} {'Days':<6} {'Fee($)':<10} {'Status':<12}")
        print("-" * 90)
        
        for booking in bookings:
            car_info = f"{booking['make']} {booking['model']} ({booking['year']})"
            print(f"{booking['booking_id']:<6} {car_info:<20} {booking['rental_start_date']:<14} {booking['rental_end_date']:<14} {booking['total_days']:<6} {booking['total_fee']:<10.2f} {booking['status']:<12}")
        
        print("\n" + "="*50)

