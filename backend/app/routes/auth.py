# app/routes/auth.py

from datetime import timedelta, datetime, timezone
from typing import Optional, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session # type: ignore
from jose import JWTError, jwt # type: ignore

from app import models, schemas, crud
from app.database import get_db
from app.core.config import settings

from passlib.context import CryptContext # type: ignore

router = APIRouter()

# Configuração de segurança para JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

oauth2_scheme_cliente = OAuth2PasswordBearer(tokenUrl="token_cliente")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# As configurações são lidas do arquivo core/config.py
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 300

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Endpoint de login
@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_salao_by_email(db, email=form_data.username)

    if not user or not verify_password(form_data.password, user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Dependência para autenticar o salão
def authenticate_salao(db: Session, email: str, senha: str):
    salao = crud.get_salao_by_email(db, email=email)
    if not salao or not verify_password(senha, salao.senha_hash):
        return False
    return salao

# Dependência para obter o salão autenticado
async def get_current_salao(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception

    salao = crud.get_salao_by_email(db, email=token_data.email)
    if salao is None:
        raise credentials_exception
    return salao

def get_current_active_salao(current_salao: models.Salao = Depends(get_current_salao)):
    if not current_salao:
        raise HTTPException(status_code=400, detail="Salão inativo")
    return current_salao

def get_password_hash(password: str):
    return pwd_context.hash(password)



# Dependência para obter o profissional autenticado
async def get_current_active_profissional(
     token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception

    profissional = crud.get_profissional_by_email(db, email=token_data.email)
    if profissional is None:
        raise credentials_exception
    return profissional


# Dependência para obter o cliente autenticado

def authenticate_cliente(db: Session, email: str, senha: str):
    cliente = crud.get_cliente_by_email(db, email=email)
    if not cliente or not verify_password(senha, cliente.senha_hash):
        return False
    return cliente

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_cliente(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme_cliente)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    cliente = crud.get_cliente_by_email(db, email=email)
    if cliente is None:
        raise credentials_exception
    return cliente

def get_current_active_cliente(current_cliente: Annotated[models.Cliente, Depends(get_current_cliente)]):
    if not current_cliente.is_active:
        raise HTTPException(status_code=400, detail="Conta do cliente inativa")
    return current_cliente