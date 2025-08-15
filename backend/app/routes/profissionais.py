# app/routes/profissionais.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session # type: ignore
from typing import List

from app import schemas, crud, models
from app.database import get_db
from .auth import get_current_active_salao

router = APIRouter(
    prefix="/profissionais",
    tags=["Profissionais"]
)

@router.post("/", response_model=schemas.Profissional, status_code=status.HTTP_201_CREATED)
def create_profissional(
    profissional: schemas.ProfissionalCreate,
    db: Session = Depends(get_db),
    current_salao: models.Salao = Depends(get_current_active_salao)
):
    if profissional.salao_id != current_salao.id:
        raise HTTPException(status_code=403, detail="Não autorizado a criar profissionais para este salão")

    db_profissional = crud.get_profissional_by_email(db, email=profissional.email)
    if db_profissional:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
        
    return crud.create_profissional(db=db, profissional=profissional)

@router.get("/", response_model=List[schemas.Profissional])
def read_profissionais(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_salao: models.Salao = Depends(get_current_active_salao)
):
    profissionais = crud.get_profissionais_by_salao(db, salao_id=current_salao.id, skip=skip, limit=limit)
    return profissionais

@router.get("/{profissional_id}", response_model=schemas.Profissional)
def read_profissional(
    profissional_id: int, 
    db: Session = Depends(get_db),
    current_salao: models.Salao = Depends(get_current_active_salao)
):
    db_profissional = crud.get_profissional(db, profissional_id=profissional_id)
    if db_profissional is None or db_profissional.salao_id != current_salao.id:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")
    return db_profissional

@router.put("/{profissional_id}", response_model=schemas.Profissional)
def update_profissional(
    profissional_id: int, 
    profissional: schemas.ProfissionalUpdate,
    db: Session = Depends(get_db),
    current_salao: models.Salao = Depends(get_current_active_salao)
):
    db_profissional = crud.get_profissional(db, profissional_id=profissional_id)
    if db_profissional is None or db_profissional.salao_id != current_salao.id:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")
        
    return crud.update_profissional(db=db, profissional_id=profissional_id, profissional=profissional)
    
@router.delete("/{profissional_id}")
def delete_profissional(
    profissional_id: int, 
    db: Session = Depends(get_db),
    current_salao: models.Salao = Depends(get_current_active_salao)
):
    db_profissional = crud.get_profissional(db, profissional_id=profissional_id)
    if db_profissional is None or db_profissional.salao_id != current_salao.id:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")
        
    crud.delete_profissional(db=db, profissional_id=profissional_id)
    return {"message": "Profissional deletado com sucesso"}