import jwt
from passlib.hash import pbkdf2_sha256
from config import SECRET_KEY


def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pbkdf2_sha256.verify(password, hashed)


def jwt_generate(payload: dict) -> str:
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def decode_payload(token: str) -> dict:
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded  
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
