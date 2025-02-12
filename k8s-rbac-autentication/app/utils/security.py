from datetime import datetime, timedelta
from jose import JWTError, jwt # type: ignore
from passlib.context import CryptContext # type: ignore
from fastapi import HTTPException, status # type: ignore
import re

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

def is_valid_password(password: str) -> bool:
    """
    Função para validar se a senha atende aos critérios de segurança.
    Exemplo de critérios: mínimo de 8 caracteres, pelo menos 1 número, 1 letra maiúscula e 1 caractere especial.
    """
    if len(password) < 8:
        return False
    if not re.search(r"\d", password):  # Verifica se há pelo menos um número
        return False
    if not re.search(r"[A-Z]", password):  # Verifica se há pelo menos uma letra maiúscula
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):  # Verifica se há pelo menos um caractere especial
        return False
    return True
