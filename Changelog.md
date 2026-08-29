# Changelog

All notable changes to the Car Rental System will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2024-08-27

### Added
- **Password Change Functionality**
  - Admin users can change password from admin menu
  - Customer users can change password from customer menu
  - Password confirmation and validation
  - Old password verification before change
  - Secure password hashing with SHA-256

- **Booking Completion Feature**
  - Admin can mark bookings as completed (returned)
  - Automatic car availability update on completion
  - Late fee calculation for overdue rentals

- **Comprehensive Date Validation**
  - Past date booking prevention
  - Zero-day booking prevention
  - Start date must be today or future
  - End date must be after start date
  - Minimum 1 day booking duration

- **Phone Validation**
  - Phone number validation during registration
  - Basic format checking for phone numbers

- **Interactive Admin Setup**
  - Admin account creation on first run
  - Password confirmation during admin creation

- **Unit Tests**
  - Test isolation with unique databases

### Fixed
- **Car Availability Logic**
  - Approved bookings now make cars unavailable
  - Rejected bookings now make cars available again

- **Late Fee Calculation**
  - Added late fee calculation on booking completion
  - Late fee = days_late × late_fee_per_day

- **Past Date Booking**
  - Prevented bookings for dates in the past
  - Added validation against current date

- **Zero-Day Booking**
  - Blocked bookings with 0 days duration
  - Minimum 1 day booking required

- **Phone Validation (Bug #7)**
  - Added phone validation during registration
  - Validator now properly used

### Security
- Password hashing using SHA-256
- Input validation for all user inputs
- SQL injection prevention using parameterized queries
- Old password verification for password changes

### Changed
- Admin account creation: Now interactive with user input
- Booking management: Enhanced with status validation
- Test isolation: Each test now uses unique database

---

## [1.0.0] - 2024-08-26

### Added
- **User Management**
  - User registration with validation
  - Secure login with password hashing
  - Role-based access (Admin/Customer)
  - Session management

- **Car Management (Admin)**
  - Add new cars to inventory
  - Update car details
  - Delete cars with booking validation
  - View all cars in system

- **Rental Booking (Customers)**
  - View available cars with details
  - Book a car with date selection
  - Automatic fee calculation
  - View booking history with status

- **Rental Management (Admin)**
  - Approve or reject pending bookings
  - View all bookings in system

- **Database**
  - SQLite database with three tables (users, cars, bookings)
  - Automatic database creation on first run

- **Testing**
  - Unit tests for authentication and rental services

### Security
- Password hashing using SHA-256
- SQL injection prevention using parameterized queries
- Input validation for user inputs

---

## [0.1.0] - 2024-08-20

### Added
- Initial release
- Basic user authentication
- Car inventory management
- Simple booking system
- Command-line interface
- Default admin account (admin/admin123)

---

## Version Comparison

| Version | Date | Type | Summary |
|---------|------|------|---------|
| **1.1.0** | 2024-08-27 | Minor | Bug fixes |
| **1.0.0** | 2024-08-26 | Major | Initial stable release |
| **0.1.0** | 2024-08-20 | Beta | Initial development |

---

## Upcoming Features

### Version 1.2.0 (Planned - Q1 2025)
- Web interface (Flask)
- REST API endpoints
- Email notifications

### Version 1.3.0 (Planned - Q2 2025)
- Payment processing
- Mobile app integration

### Version 2.0.0 (Planned - Q3 2025)
- Microservices architecture
- Cloud deployment
- AI-powered recommendations

---


**Last Updated:** August 2024