# backend/app/routes/agendamentos.py (ou o nome do seu arquivo de rotas)

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session  # type: ignore

from app import schemas, crud
from app.database import get_db

app = APIRouter()

# Endpoint para criar um agendamento
@app.post("/", response_model=schemas.Agendamento, status_code=status.HTTP_201_CREATED)
def create_agendamento(agendamento: schemas.AgendamentoCreate, db: Session = Depends(get_db)):
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

# Endpoint para listar agendamentos
@app.get("/", response_model=List[schemas.Agendamento])
def read_agendamentos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    agendamentos = crud.get_agendamentos(db, skip=skip, limit=limit)
    return agendamentos
# Endpoint para obter um agendamento por ID
@app.get("/{agendamento_id}", response_model=schemas.Agendamento)
def read_agendamento(agendamento_id: int, db: Session = Depends(get_db)):
    db_agendamento = crud.get_agendamento(db, agendamento_id=agendamento_id)
    if db_agendamento is None:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    return db_agendamento
# Endpoint para atualizar um agendamento
@app.put("/{agendamento_id}", response_model=schemas.Agendamento)
def update_agendamento(agendamento_id: int, agendamento: schemas.AgendamentoUpdate
                        , db: Session = Depends(get_db)):
    db_agendamento = crud.get_agendamento(db, agendamento_id=agendamento_id)
    if db_agendamento is None:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    return crud.update_agendamento(db=db, agendamento_id=agendamento_id, agendamento=agendamento)
# Endpoint para deletar um agendamento
@app.delete("/{agendamento_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agendamento(agendamento_id: int, db: Session = Depends(get_db)):
    db_agendamento = crud.get_agendamento(db, agendamento_id=agendamento_id)
    if db_agendamento is None:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    crud.delete_agendamento(db=db, agendamento_id=agendamento_id)
    return {"detail": "Agendamento deletado com sucesso"}