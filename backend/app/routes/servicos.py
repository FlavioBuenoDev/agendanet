# app/routes/servicos.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session # type: ignore
from typing import List

from app import schemas, crud, models
from app.database import get_db
from .auth import get_current_active_salao

router = APIRouter(
    prefix="/servicos",
    tags=["Serviços"]
)

@router.post("/", response_model=schemas.ServicoRead, status_code=status.HTTP_201_CREATED)
def create_servico_for_salao(
    servico: schemas.ServicoCreate,
    db: Session = Depends(get_db),
    current_salao: models.Salao = Depends(get_current_active_salao)
):
    if servico.salao_id != current_salao.id:
        raise HTTPException(status_code=403, detail="Não autorizado a criar serviços para este salão")
        
    return crud.create_servico(db=db, servico=servico)

@router.get("/", response_model=List[schemas.ServicoRead])
def read_servicos(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_salao: models.Salao = Depends(get_current_active_salao)
):
    servicos = crud.get_servicos_by_salao(db, salao_id=current_salao.id, skip=skip, limit=limit)
    return servicos

@router.get("/{servico_id}", response_model=schemas.ServicoRead)
def read_servico(
    servico_id: int, 
    db: Session = Depends(get_db),
    current_salao: models.Salao = Depends(get_current_active_salao)
):
    db_servico = crud.get_servico(db, servico_id=servico_id)
    if db_servico is None or db_servico.salao_id != current_salao.id:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return db_servico

@router.put("/{servico_id}", response_model=schemas.ServicoRead)
def update_servico(
    servico_id: int, 
    servico: schemas.ServicoUpdate,
    db: Session = Depends(get_db),
    current_salao: models.Salao = Depends(get_current_active_salao)
):
    db_servico = crud.get_servico(db, servico_id=servico_id)
    if db_servico is None or db_servico.salao_id != current_salao.id:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
        
    return crud.update_servico(db=db, servico_id=servico_id, servico=servico)
    
@router.delete("/{servico_id}")
def delete_servico(
    servico_id: int, 
    db: Session = Depends(get_db),
    current_salao: models.Salao = Depends(get_current_active_salao)
):
    db_servico = crud.get_servico(db, servico_id=servico_id)
    if db_servico is None or db_servico.salao_id != current_salao.id:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
        
    crud.delete_servico(db=db, servico_id=servico_id)
    return {"message": "Serviço deletado com sucesso"}