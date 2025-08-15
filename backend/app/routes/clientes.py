# app/routes/clientes.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session # type: ignore
from datetime import timedelta
from typing import Annotated, List

from app import schemas, crud, models
from app.database import get_db
from .auth import (
    authenticate_cliente, 
    create_access_token, 
    get_current_active_cliente
)

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)

@router.post("/", response_model=schemas.Cliente, status_code=status.HTTP_201_CREATED)
def create_cliente(
    cliente: schemas.ClienteCreate,
    db: Session = Depends(get_db)
):
    db_cliente = crud.get_cliente_by_email(db, email=cliente.email)
    if db_cliente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    return crud.create_cliente(db=db, cliente=cliente)

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    db: Session = Depends(get_db)
):
    cliente = authenticate_cliente(db, form_data.username, form_data.password)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": cliente.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me/", response_model=schemas.Cliente)
async def read_clientes_me(current_cliente: Annotated[models.Cliente, Depends(get_current_active_cliente)]):
    return current_cliente

@router.get("/", response_model=List[schemas.Cliente])
def read_clientes(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    clientes = crud.get_clientes(db, skip=skip, limit=limit)
    return clientes

@router.get("/{cliente_id}", response_model=schemas.Cliente)
def read_cliente(
    cliente_id: int, 
    db: Session = Depends(get_db)
):
    db_cliente = crud.get_cliente(db, cliente_id=cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return db_cliente

@router.put("/{cliente_id}", response_model=schemas.Cliente)
def update_cliente(
    cliente_id: int, 
    cliente: schemas.ClienteUpdate,
    db: Session = Depends(get_db),
    current_cliente: Annotated[models.Cliente, Depends(get_current_active_cliente)] = None
):
    if cliente_id != current_cliente.id:
        raise HTTPException(status_code=403, detail="Não autorizado a atualizar este cliente")
    
    db_cliente = crud.update_cliente(db=db, cliente_id=cliente_id, cliente=cliente)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return db_cliente

@router.delete("/{cliente_id}")
def delete_cliente(
    cliente_id: int, 
    db: Session = Depends(get_db),
    current_cliente: Annotated[models.Cliente, Depends(get_current_active_cliente)] = None
):
    if cliente_id != current_cliente.id:
        raise HTTPException(status_code=403, detail="Não autorizado a deletar este cliente")
        
    db_cliente = crud.delete_cliente(db=db, cliente_id=cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return {"message": "Cliente deletado com sucesso"}