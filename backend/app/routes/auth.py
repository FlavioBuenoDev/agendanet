# backend/app/routes/auth.py

from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session # type: ignore
from datetime import timedelta
from app import schemas, crud
from app.database import get_db
from app.core.security import create_access_token, verify_password, decode_token
from app.core.config import settings
from app.models import Salao, Profissional, Cliente # Importe os modelos

router = APIRouter()     
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Autentica um usuário (salão, profissional ou cliente) e retorna um token JWT.
    """
    user = crud.get_salao_by_email(db, email=form_data.username)
    user_type = "salao"

    if not user:
        user = crud.get_profissional_by_email(db, email=form_data.username)
        user_type = "profissional"
    
    if not user:
        user = crud.get_cliente_by_email(db, email=form_data.username)
        user_type = "cliente"
    
    if not user or not verify_password(form_data.password, user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_type": user_type}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Decodifica o token e retorna o usuário atual.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    
    email = payload.get("sub")
    user_type = payload.get("user_type")
    
    if email is None or user_type is None:
        raise credentials_exception
    
    if user_type == "salao":
        user = crud.get_salao_by_email(db, email=email)
    elif user_type == "profissional":
        user = crud.get_profissional_by_email(db, email=email)
    elif user_type == "cliente":
        user = crud.get_cliente_by_email(db, email=email)
    else:
        user = None

    if user is None:
        raise credentials_exception
    
    return user, user_type

def get_current_active_salao(current_user_data: tuple = Depends(get_current_user)):
    """
    Dependência para obter um salão ativo.
    """
    user, user_type = current_user_data
    if user_type != "salao":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas salões podem realizar esta ação."
        )
   
    return user

def get_current_active_profissional(current_user_data: tuple = Depends(get_current_user)):
    """
    Dependência para obter um profissional ativo.
    """
    user, user_type = current_user_data
    if user_type != "profissional":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas profissionais podem realizar esta ação."
        )
    return user

def get_current_active_cliente(current_user_data: tuple = Depends(get_current_user)):
    """
    Dependência para obter um cliente ativo.
    """
    user, user_type = current_user_data
    if user_type != "cliente":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas clientes podem realizar esta ação."
        )
    # A verificação 'is_active' pode ser adicionada se houver um campo no modelo
    # if not user.is_active:
    #     raise HTTPException(status_code=400, detail="Cliente inativo")
    return user
