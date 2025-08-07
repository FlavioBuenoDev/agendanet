# app/routes/clientes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session # type: ignore
from sqlalchemy.exc import IntegrityError # type: ignore
from .. import crud, schemas
from ..database import get_db
from typing import List

router = APIRouter()

# Endpoint para criar um cliente (VERSÃO CORRIGIDA E COMBINADA)
@router.post("/", response_model=schemas.Cliente, status_code=status.HTTP_201_CREATED)
def create_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = crud.get_cliente_by_email(db, email=cliente.email)
    if db_cliente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já cadastrado."
        )
    return crud.create_cliente(db=db, cliente=cliente)

# Endpoint para listar clientes
@router.get("/", response_model=List[schemas.Cliente])
def read_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clientes = crud.get_clientes(db, skip=skip, limit=limit)
    return clientes

# Endpoint para obter um cliente por ID
@router.get("/{cliente_id}", response_model=schemas.Cliente)
def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = crud.get_cliente(db, cliente_id=cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return db_cliente

# Endpoint para atualizar um cliente
@router.put("/{cliente_id}", response_model=schemas.Cliente)
def update_cliente(cliente_id: int, cliente: schemas.ClienteUpdate, db: Session = Depends(get_db)):
    db_cliente = crud.get_cliente(db, cliente_id=cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return crud.update_cliente(db=db, cliente_id=cliente_id, cliente=cliente)

# Endpoint para deletar um cliente
@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = crud.get_cliente(db, cliente_id=cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    crud.delete_cliente(db=db, cliente_id=cliente_id)
    return {"detail": "Cliente deletado com sucesso"}