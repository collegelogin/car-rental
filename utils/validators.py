import re
class Validators:
    @staticmethod
    def validate_email(email):
        #this is to validate email
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
