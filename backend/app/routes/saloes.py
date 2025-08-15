from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session # type: ignore
from typing import Annotated, List

from app import schemas, crud, models
from .auth import create_access_token, get_current_active_salao, authenticate_salao
from app.database import get_db

router = APIRouter(
    prefix="/saloes",
    tags=["Salões"]
)

# Rota para obter token do salão
@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    salao = authenticate_salao(db, form_data.username, form_data.password) # type: ignore
    if not salao:
        raise HTTPException(...)
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": salao.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint para obter informações do salão autenticado
@router.get("/me/", response_model=schemas.Salao)
def read_salao_me(current_salao: models.Salao = Depends(get_current_active_salao)):
    return current_salao

# Endpoint para criar um salão (rota pública)
@router.post("/", response_model=schemas.Salao, status_code=status.HTTP_201_CREATED)
def create_salao(salao: schemas.SalaoCreate, db: Session = Depends(get_db)):
    db_salao = crud.get_salao_by_email(db, email=salao.email)
    if db_salao:
        raise HTTPException(status_code=400, detail="Email já registrado")
    return crud.create_salao(db=db, salao=salao)

# Endpoint para listar salões (rota pública)
@router.get("/", response_model=List[schemas.Salao])
def read_saloes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    saloes = crud.get_saloes(db, skip=skip, limit=limit)
    return saloes

# Endpoint para obter um salão por ID (rota pública, apenas para leitura)
@router.get("/{salao_id}", response_model=schemas.Salao)
def read_salao(salao_id: int, db: Session = Depends(get_db)):
    db_salao = crud.get_salao(db, salao_id=salao_id)
    if db_salao is None:
        raise HTTPException(status_code=404, detail="Salão não encontrado")
    return db_salao

# Endpoint para atualizar o salão autenticado
@router.put("/{salao_id}", response_model=schemas.Salao)
def update_salao(
    salao_id: int, 
    salao: schemas.SalaoUpdate, 
    db: Session = Depends(get_db),
    current_salao: models.Salao = Depends(get_current_active_salao)
):
    if salao_id != current_salao.id:
        raise HTTPException(status_code=403, detail="Não autorizado a atualizar este salão")
    
    db_salao = crud.get_salao(db, salao_id=salao_id)
    if db_salao is None:
        raise HTTPException(status_code=404, detail="Salão não encontrado")
    return crud.update_salao(db=db, salao_id=salao_id, salao=salao)

# Endpoint para deletar o salão autenticado
@router.delete("/{salao_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_salao(
    salao_id: int, 
    db: Session = Depends(get_db),
    current_salao: models.Salao = Depends(get_current_active_salao)
):
    if salao_id != current_salao.id:
        raise HTTPException(status_code=403, detail="Não autorizado a deletar este salão")

    db_salao = crud.get_salao(db, salao_id=salao_id)
    if db_salao is None:
        raise HTTPException(status_code=404, detail="Salão não encontrado")
    
    crud.delete_salao(db=db, salao_id=salao_id)
    return {"detail": "Salão deletado com sucesso"}