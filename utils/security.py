import hashlib
class SecurityUtils:
    
    @staticmethod
    def hash_password(password):
        #this is for password hashing
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password, hashed_password):
        #this is for password verification
        return SecurityUtils.hash_password(password) == hashed_password
