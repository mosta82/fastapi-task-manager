import bcrypt

class Hash:
    @staticmethod
    def bcrypt(password: str):
        # password hashing using bcrypt
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(pwd_bytes, salt)
        return hashed_password.decode('utf-8')

    @staticmethod
    def verify(plain_password, hashed_password):
        # logic to verify a plain password against a hashed password
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))