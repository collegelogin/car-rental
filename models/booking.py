class Booking:
    def __init__(self, booking_id=None, car_id=None, customer_id=None,
                 booking_date=None, rental_start_date=None, rental_end_date=None,
                 total_days=None, daily_rate=None, total_fee=None,
                 status=None, admin_notes=None, created_date=None):
        self.booking_id = booking_id
        self.car_id = car_id
        self.customer_id = customer_id
        self.booking_date = booking_date
        self.rental_start_date = rental_start_date
        self.rental_end_date = rental_end_date
        self.total_days = total_days
        self.daily_rate = daily_rate
        self.total_fee = total_fee
        self.status = status
        self.admin_notes = admin_notes
        self.created_date = created_date
    
    @staticmethod
    def from_db_row(row):
        if not row:
            return None
        return Booking(
            booking_id=row[0],
            car_id=row[1],
            customer_id=row[2],
            booking_date=row[3],
            rental_start_date=row[4],
            rental_end_date=row[5],
            total_days=row[6],
            daily_rate=row[7],
            total_fee=row[8],
            status=row[9],
            admin_notes=row[10] if len(row) > 10 else None,
            created_date=row[11] if len(row) > 11 else None
        )
