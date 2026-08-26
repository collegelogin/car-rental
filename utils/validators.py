import re
class Validators:
    @staticmethod
    def validate_email(email):
        #this is to validate email
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_phone(phone):
        #this is to validate phone number
        pattern = r'^[\d\s\-+()]{7,15}$'
        return re.match(pattern, phone) is not None
        
    @staticmethod
    def validate_date(date_str):
        #this is to validate date format
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(pattern, date_str):
            return False
        try:
            from datetime import datetime
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
