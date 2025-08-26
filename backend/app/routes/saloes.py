# backend/app/routes/saloes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session # type: ignore
from typing import List

from app.database import get_db
from app import schemas, crud, models
from app.core.security import create_access_token
from datetime import timedelta
from app.core.config import settings

from app.core.security import get_password_hash # Importe a função de hash

router = APIRouter(
    prefix="/saloes",
    tags=["saloes"],
)

@router.post("/", response_model=schemas.SalaoRead, status_code=status.HTTP_201_CREATED)
def create_salao(salao: schemas.SalaoCreate, db: Session = Depends(get_db)):
    """
    Cria um novo salão.
    """
    db_salao = crud.get_salao_by_email(db, email=salao.email)
    if db_salao:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    # Hasheia a senha antes de passar para a função CRUD
    hashed_password = get_password_hash(salao.senha)
    
    # Cria uma cópia dos dados de entrada, mas com a senha hasheada
    salao_data = salao.model_dump()
    salao_data["senha"] = hashed_password
    
    # Cria o salão no banco de dados com a senha hasheada
    return crud.create_salao(db=db, salao=schemas.SalaoCreate(**salao_data))

@router.get("/", response_model=List[schemas.SalaoRead])
def read_saloes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    saloes = crud.get_saloes(db, skip=skip, limit=limit)
    return saloes

@router.get("/{salao_id}", response_model=schemas.SalaoRead)
def read_salao(salao_id: int, db: Session = Depends(get_db)):
    db_salao = crud.get_salao(db, salao_id=salao_id)
    if db_salao is None:
        raise HTTPException(status_code=404, detail="Salão não encontrado")
    return db_salao