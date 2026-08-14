from datetime import datetime, timedelta
from jose import JWTError, jwt

# secret key, algorithm, and token expiration time configuration
SECRET_KEY = "your_super_secret_key_here_change_it"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # token expiration time in minutes
def create_access_token(data: dict):
    to_encode = data.copy()
    # token expiration time set to current time + ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # token encoding using the secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt