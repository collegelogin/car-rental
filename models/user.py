class User:
    def __init__(self, user_id=None, username=None, password=None, 
                 full_name=None, email=None, phone=None, role=None, 
                 created_date=None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.role = role
        self.created_date = created_date
    
    def to_dict(self):
        #converting user object to dictionary
        return {
            'user_id': self.user_id,
            'username': self.username,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'created_date': self.created_date
        }
    
    @staticmethod
    def from_db_row(row):
        #create database object from row
        if not row:
            return None
        return User(
            user_id=row[0],
            username=row[1],
            password=row[2],
            full_name=row[3],
            email=row[4],
            phone=row[5],
            role=row[6],
            created_date=row[7]
        )
