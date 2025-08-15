from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session  # type: ignore
from typing import List

from app import schemas, crud, models
from .auth import get_current_active_salao
from app.database import get_db

router = APIRouter()

# Endpoint para obter informações do salão autenticado
@router.get("/me/", response_model=schemas.Salao)
def read_salao_me(current_salao: models.Salao = Depends(get_current_active_salao)):
    return current_salao

# Endpoint para criar um salão
@router.post("/", response_model=schemas.Salao, status_code=status.HTTP_201_CREATED) # type: ignore
def create_salao(salao: schemas.SalaoCreate, db: Session = Depends(get_db)):
    db_salao = crud.get_salao_by_email(db, email=salao.email)
    if db_salao:
        raise HTTPException(status_code=400, detail="Email já registrado")
    return crud.create_salao(db=db, salao=salao)

# Endpoint para listar salões
@router.get("/", response_model=List[schemas.Salao]) # type: ignore
def read_saloes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    saloes = crud.get_saloes(db, skip=skip, limit=limit)
    return saloes

# Endpoint para obter um salão por ID
@router.get("/{salao_id}", response_model=schemas.Salao) # type: ignore
def read_salao(salao_id: int, db: Session = Depends(get_db)):
    db_salao = crud.get_salao(db, salao_id=salao_id)
    if db_salao is None:
        raise HTTPException(status_code=404, detail="Salão não encontrado")
    return db_salao

# Endpoint para atualizar um salão
@router.put("/{salao_id}", response_model=schemas.Salao) # type: ignore
def update_salao(salao_id: int, salao: schemas.SalaoUpdate, db: Session = Depends(get_db)):
    db_salao = crud.get_salao(db, salao_id=salao_id)
    if db_salao is None:
        raise HTTPException(status_code=404, detail="Salão não encontrado")
    return crud.update_salao(db=db, salao_id=salao_id, salao=salao)

# Endpoint para deletar um salão
@router.delete("/{salao_id}", status_code=status.HTTP_204_NO_CONTENT) # type: ignore
def delete_salao(salao_id: int, db: Session = Depends(get_db)):
    db_salao = crud.get_salao(db, salao_id=salao_id)
    if db_salao is None:
        raise HTTPException(status_code=404, detail="Salão não encontrado")
    crud.delete_salao(db=db, salao_id=salao_id)
    return {"detail": "Salão deletado com sucesso"}