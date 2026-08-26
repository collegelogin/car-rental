class Car:
    def __init__(self, car_id=None, make=None, model=None, year=None,
                 mileage=None, available_now=None, min_rent_period=None,
                 max_rent_period=None, daily_rate=None, late_fee_per_day=None,
                 created_date=None):
        self.car_id = car_id
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.available_now = available_now
        self.min_rent_period = min_rent_period
        self.max_rent_period = max_rent_period
        self.daily_rate = daily_rate
        self.late_fee_per_day = late_fee_per_day
        self.created_date = created_date
    
    def get_full_name(self):
        return f"{self.make} {self.model} ({self.year})"
    
    def is_available(self):
        return self.available_now == 'yes'
    
    @staticmethod
    def from_db_row(row):
        if not row:
            return None
        return Car(
            car_id=row[0],
            make=row[1],
            model=row[2],
            year=row[3],
            mileage=row[4],
            available_now=row[5],
            min_rent_period=row[6],
            max_rent_period=row[7],
            daily_rate=row[8],
            late_fee_per_day=row[9],
            created_date=row[10] if len(row) > 10 else None
        )
