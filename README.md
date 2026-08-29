# Car Rental System

A comprehensive car rental management system built with Python and SQLite.

---

## Overview

The Car Rental System is a command-line application designed to automate car rental operations. It replaces manual paperwork with a digital system that handles user management, car inventory, rental bookings, and administrative approvals.

---

## Features

### User Management

- User registration with validation
- Secure login with password hashing (SHA-256)
- Role-based access (Admin/Customer)
- Password change functionality

### Car Management (Admin Only)

- Add new cars to inventory
- Update car details
- Delete cars (with booking validation)
- View all cars in system

### Rental Booking (Customers)

- View available cars with details
- Book a car with date selection
- Automatic fee calculation
- View booking history with status

### Rental Management (Admin Only)

- Approve or reject pending bookings
- Complete bookings (mark as returned)
- Late fee calculation
- View all bookings in system

---

## Installation

### Prerequisites

- Python 3.14.6
- No external packages needed (uses only Python standard library)

### Step 1: Download the Source Code

#### Option A: Clone from GitHub

```bash
git clone https://github.com/collegelogin/car-rental
cd car-rental
```

#### Option B: Download ZIP

1. Go to https://github.com/collegelogin/car-rental
2. Click **Code** → **Download ZIP**
3. Extract the ZIP file
4. Navigate to the extracted folder

### Step 2: Verify Python Installation

```bash
python3 --version
# Should show Python 3.14.6 
```

### Step 3: Run the Application

```bash
python3 main.py
```

### Step 4: Default Admin Account

On first run, a default admin account is automatically created:

```text
   Default admin created!
   Username: admin
   Password: admin123
   Please change password after first login!
```

**Default Admin Credentials:**

- **Username:** `admin`
- **Password:** `admin123`

> ⚠️ **Important:** Change the default password immediately after first login for security reasons.

---

##  How to Use the System

### Main Menu

When you start the application, you'll see:

```text
==================================================
   CAR RENTAL SYSTEM
==================================================
1. Register
2. Login
3. Exit
==================================================
```

### For Customers

#### Step 1: Register or Login

- **New User:** Select option 1 and fill in your details
- **Existing User:** Select option 2 and login

#### Step 2: View Available Cars

```text
Customer Menu → 1. View Available Cars
```

This shows all cars available for rent with:

- Car ID, Make, Model, Year
- Mileage, Daily Rate
- Minimum/Maximum rent period

#### Step 3: Book a Car

```text
Customer Menu → 2. Book a Car
```

1. Enter the Car ID from the available list
2. Enter rental start date (YYYY-MM-DD)
3. Enter rental end date (YYYY-MM-DD)
4. Confirm the booking

**Example:**

```text
Enter Car ID to book: 1
Enter rental start date (YYYY-MM-DD): 2024-09-01
Enter rental end date (YYYY-MM-DD): 2024-09-05

   Booking Summary:
   Rental Period: 4 days
   Daily Rate: $50.00
   Total Fee: $200.00

Confirm booking? (yes/no): yes
Booking created successfully with ID: 1
```

#### Step 4: Check Your Bookings

```text
Customer Menu → 3. View My Bookings
```

Shows all your bookings with status:

- `pending`
- `approved`
- `rejected`
- `completed`

#### Step 5: Change Password

```text
Customer Menu → 4. Change Password
```

Enter your current password and new password.

### For Admins

#### Login as Admin

Use the default admin credentials:

- **Username:** `admin`
- **Password:** `admin123`

#### Manage Cars

```text
Admin Menu → 1. View All Cars        # See all cars
Admin Menu → 2. Add New Car          # Add a car to inventory
Admin Menu → 3. Update Car           # Modify car details
Admin Menu → 4. Delete Car           # Remove a car (no bookings)
```

#### Add a New Car Example

```text
Enter car make (e.g., Toyota): Toyota
Enter car model (e.g., Camry): Camry
Enter year (e.g., 2020): 2020
Enter mileage (km): 15000
Is car available now? (yes/no): yes
Enter minimum rent period (days): 2
Enter maximum rent period (days): 7
Enter daily rate ($): 55.00
Enter late fee per day ($): 25.00

Car added successfully with ID: 5
```

#### Manage Bookings

```text
Admin Menu → 5. Manage Bookings
```

1. **Approve:** Accept a pending booking → Car becomes unavailable
2. **Reject:** Decline a booking with reason → Car becomes available
3. **Complete:** Mark as returned → Late fee calculated if overdue

#### View All Bookings

```text
Admin Menu → 6. View All Bookings
```

Shows all bookings in the system with customer names, car details, and status.

#### Change Password

```text
Admin Menu → 7. Change Password
```

---

## File Structure & Purposes

```text
car_rental_system/
├── main.py                    # Application entry point - starts the program
├── requirements.txt           # List of Python dependencies (uses only standard library)
├── README.md                  # This file - user and programmer documentation
├── LICENSE                    # MIT License - terms of use
├── CHANGELOG.md               # Version history and release notes
│
├── models/                    # Data models (business objects)
│   ├── __init__.py            # Makes models a Python package
│   ├── user.py                # User class - handles user data
│   ├── car.py                 # Car class - handles car data
│   └── booking.py             # Booking class - handles booking data
│
├── services/                  # Business logic layer
│   ├── __init__.py            # Makes services a Python package
│   ├── auth_service.py        # Authentication logic (login, register, password)
│   ├── rental_service.py      # Rental operations (bookings, cars, fees)
│   └── db_service.py          # Database operations (SQLite connection, queries)
│
├── utils/                     # Utility functions
│   ├── __init__.py            # Makes utils a Python package
│   ├── security.py            # Password hashing (SHA-256)
│   └── validators.py           # Input validation (email, phone, dates)
│
├── ui/                        # User interface layer
│   ├── __init__.py            # Makes ui a Python package
│   ├── main_menu.py           # Main menu (register, login, exit)
│   ├── admin_menu.py          # Admin menu (all admin functions)
│   └── customer_menu.py       # Customer menu (booking, viewing)
│
├── tests/                     # Unit tests
│   ├── __init__.py            # Makes tests a Python package
│   ├── test_auth.py           # Tests for authentication
│   └── test_rental.py         # Tests for rental operations
│   
│
└── car_rental.db              # SQLite database (created automatically)
```

### Purpose of Each Directory

| Directory | Purpose |
|---|---|
| **models/** | Contains classes that represent real-world objects (User, Car, Booking). These are the "data" objects. |
| **services/** | Contains the business logic. This is where the "work" happens - authentication, rentals, database access. |
| **utils/** | Helper functions that are used across the system (security, validation). |
| **ui/** | User interface - handles all input/output with the user via the command line. |
| **tests/** | Unit tests to verify the system works correctly. |

---

##  License

This project is licensed under the **MIT License**.

**MIT License Summary:**

- ✅ You can freely use, modify, and distribute this software
- ✅ Commercial use is allowed
- ✅ You must include the original copyright notice
- ❌ No warranty is provided - use at your own risk

Full license text is available in the [LICENSE](LICENSE) file.

---

## Known Bugs and Issues

### No Critical Issues

All known bugs have been fixed in version 1.1.0. The system is stable and production-ready.

### Minor Limitations

| Issue | Severity | Status | Future Fix |
|---|---|---|---|
| No web interface | Low | Not implemented | Future release |
| No email notifications | Low | Not implemented | Future release |
| No payment processing | Medium | Not implemented | Future release |
| No mobile app | Low | Not implemented | Future release |

### Bug History (All Fixed in v1.1.0)

- ✅ Car availability logic fixed
- ✅ Late fee calculation added
- ✅ Past date booking prevented
- ✅ Zero-day booking prevented
- ✅ Booking completion added
- ✅ Database connection leaks fixed
- ✅ Phone validation added
- ✅ Password change added
- ✅ Booking status validation added

---

## Credits

### Developer

- **Sandhya Tiwari**

- **Email:** 270918511@yoobeestudent.ac.nz
- **GitHub:** https://github.com/collegelogin

### Course Information

- **Course:** Professional Software Engineering (MSE 800)
- **Institution:** Yoobee College of Creative Innovation
- **Assignment:** Car Rental System
- **Date:** August 2024



---

## Support

If you encounter any issues:

1. Check this README first
2. Search existing issues on GitHub
3. Create a new issue at: https://github.com/collegelogin/car-rental/issues

---

## Future Roadmap

| Version | Features | Target |
|---|---|---|
| **1.2.0** | Web interface (Flask) | Q1 2025 |
| **1.3.0** | Payment processing | Q2 2025 |
| **1.4.0** | Email notifications | Q3 2025 |
| **2.0.0** | Mobile app, API | Q4 2025 |

---

**Current Version:** 1.1.0  
**Release Date:** August 27, 2024  
**Status:** Stable
