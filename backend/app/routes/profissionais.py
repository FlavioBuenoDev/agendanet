
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session  # type: ignore

from app import schemas, crud # type: ignore
from app.database import get_db # type: ignore
from typing import List

router = APIRouter()

#endpoint para criar um profissional
@router.post("/", response_model=schemas.Profissional, status_code=status.HTTP_201_CREATED) # type: ignore
def create_profissional(profissional: schemas.ProfissionalCreate, db: Session = Depends(get_db)):
    db_profissional = crud.get_profissional_by_email(db, email=profissional.email)
    if db_profissional:
        raise HTTPException(status_code=400, detail="Email já registrado")
    return crud.create_profissional(db=db, profissional=profissional)

# Endpoint para listar profissionais
@router.get("/", response_model=List[schemas.Profissional]) # type: ignore
def read_profissionais(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    profissionais = crud.get_profissionais(db, skip=skip, limit=limit)
    return profissionais

# Endpoint para obter um profissional por ID
@router.get("/{profissional_id}", response_model=schemas.Profissional) # type: ignore
def read_profissional(profissional_id: int, db: Session = Depends(get_db)):
    db_profissional = crud.get_profissional(db, profissional_id=profissional_id)
    if db_profissional is None:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")
    return db_profissional

# Endpoint para atualizar um profissional
@router.put("/{profissional_id}", response_model=schemas.Profissional) # type: ignore
def update_profissional(profissional_id: int, profissional: schemas.ProfissionalUpdate,
                        db: Session = Depends(get_db)):
    db_profissional = crud.get_profissional(db, profissional_id=profissional_id)
    if db_profissional is None:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")
    return crud.update_profissional(db=db, profissional_id=profissional_id, profissional=profissional)

# Endpoint para deletar um profissional
@router.delete("/{profissional_id}", status_code=status.HTTP_204_NO_CONTENT) # type: ignore
def delete_profissional(profissional_id: int, db: Session = Depends(get_db)):
    db_profissional = crud.get_profissional(db, profissional_id=profissional_id)
    if db_profissional is None:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")
    crud.delete_profissional(db=db, profissional_id=profissional_id)
    return {"detail": "Profissional deletado com sucesso"}