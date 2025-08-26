# app/routes/agendamentos.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session # type: ignore
from typing import List, Annotated

from app import schemas, crud, models
from app.database import get_db
from .auth import get_current_active_cliente, get_current_active_profissional

router = APIRouter(
    prefix="/agendamentos",
    tags=["Agendamentos"]
)

@router.post("/", response_model=schemas.AgendamentoRead, status_code=status.HTTP_201_CREATED)
def create_agendamento(
    agendamento: schemas.AgendamentoCreate,
    db: Session = Depends(get_db),
    current_cliente: Annotated[models.Cliente, Depends(get_current_active_cliente)] = None
):
    if agendamento.cliente_id != current_cliente.id:
        raise HTTPException(status_code=403, detail="Não autorizado a criar agendamento para outro cliente")

    try:
        return crud.create_agendamento(db=db, agendamento=agendamento)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me/", response_model=List[schemas.AgendamentoRead])
def read_agendamentos_cliente(
    db: Session = Depends(get_db),
    current_cliente: Annotated[models.Cliente, Depends(get_current_active_cliente)] = None
):
    agendamentos = crud.get_agendamentos_by_cliente(db, cliente_id=current_cliente.id)
    return agendamentos
    
@router.get("/profissional/", response_model=List[schemas.AgendamentoRead])
def read_agendamentos_profissional(
    db: Session = Depends(get_db),
    current_profissional: Annotated[models.Profissional, Depends(get_current_active_profissional)] = None
):
    agendamentos = crud.get_agendamentos_by_profissional(db, profissional_id=current_profissional.id)
    return agendamentos

@router.get("/{agendamento_id}", response_model=schemas.AgendamentoRead)
def read_agendamento(
    agendamento_id: int, 
    db: Session = Depends(get_db)
):
    agendamento = crud.get_agendamento(db, agendamento_id=agendamento_id)
    if agendamento is None:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    return agendamento

@router.delete("/{agendamento_id}")
def delete_agendamento(
    agendamento_id: int, 
    db: Session = Depends(get_db),
    current_cliente: Annotated[models.Cliente, Depends(get_current_active_cliente)] = None,
    current_profissional: Annotated[models.Profissional, Depends(get_current_active_profissional)] = None
):
    db_agendamento = crud.get_agendamento(db, agendamento_id=agendamento_id)
    if not db_agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    # Autorização: Apenas o cliente ou o profissional do agendamento podem deletá-lo
    if current_cliente and db_agendamento.cliente_id != current_cliente.id:
        raise HTTPException(status_code=403, detail="Não autorizado a deletar este agendamento")
    if current_profissional and db_agendamento.profissional_id != current_profissional.id:
        raise HTTPException(status_code=403, detail="Não autorizado a deletar este agendamento")
    
    return crud.delete_agendamento(db=db, agendamento_id=agendamento_id)