# backend/app/core/security.py

from datetime import datetime, timedelta, timezone
from typing import Any
from passlib.context import CryptContext # type: ignore
from jose import jwt, JWTError # type: ignore
from app.core.config import settings

# Crie uma instância do gerenciador de hash de senhas
# Use scrypt para uma segurança moderna e robusta
pwd_context = CryptContext(schemes=["scrypt"], deprecated="auto")

# Função para obter o hash de uma senha
def get_password_hash(password: str) -> str:
    """
    Retorna o hash de uma senha usando scrypt.
    """
    return pwd_context.hash(password)

# Função para verificar uma senha em relação ao seu hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha em texto plano corresponde ao hash.
    """
    return pwd_context.verify(plain_password, hashed_password)

# Função para criar um token de acesso JWT
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Cria um token JWT com dados e tempo de expiração.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt

# Função para decodificar um token JWT
def decode_token(token: str) -> Any:
    """
    Decodifica um token JWT e retorna os dados.
    Levanta um erro se o token for inválido ou expirado.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
