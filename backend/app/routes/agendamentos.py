# backend/app/routes/agendamentos.py (ou o nome do seu arquivo de rotas)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session  # type: ignore

from app import schemas, crud
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Agendamento)
def create_agendamento(agendamento: schemas.AgendamentoCreate, db: Session = Depends(get_db)):
    
    print("--- Endpoint de agendamento acessado! ---") #(DEBUG)
    
    # 1. Verifique se há um agendamento em conflito para o profissional
    conflito = crud.get_agendamentos_conflitantes(
        db,
        profissional_id=agendamento.profissional_id,
        data_hora_inicio=agendamento.data_hora_inicio,
        data_hora_fim=agendamento.data_hora_fim
    )
    if conflito:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um agendamento para este profissional neste horário."
        )

    # 2. Se não houver conflito, crie o agendamento
    return crud.create_agendamento(db=db, agendamento=agendamento)