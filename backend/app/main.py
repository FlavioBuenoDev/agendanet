# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session # type: ignore
from typing import List

from .database import get_db
from . import models, schemas, crud # Importe o crud e os schemas

app = FastAPI(
    title="API de Agendamento Salão de Beleza",
    description="API para gerenciar agendamentos, salões, profissionais, serviços e clientes.",
    version="0.1.0",
)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Agendamento do Salão de Beleza!"}

# Endpoint para criar um salão
@app.post("/saloes/", response_model=schemas.Salao, status_code=status.HTTP_201_CREATED)
def create_salao(salao: schemas.SalaoCreate, db: Session = Depends(get_db)):
    db_salao = crud.get_salao_by_email(db, email=salao.email)
    if db_salao:
        raise HTTPException(status_code=400, detail="Email já registrado")
    return crud.create_salao(db=db, salao=salao)

# Endpoint para listar salões
@app.get("/saloes/", response_model=List[schemas.Salao])
def read_saloes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    saloes = crud.get_saloes(db, skip=skip, limit=limit)
    return saloes

# Endpoint para obter um salão por ID
@app.get("/saloes/{salao_id}", response_model=schemas.Salao)
def read_salao(salao_id: int, db: Session = Depends(get_db)):
    db_salao = crud.get_salao(db, salao_id=salao_id)
    if db_salao is None:
        raise HTTPException(status_code=404, detail="Salão não encontrado")
    return db_salao

# Endpoint para atualizar um salão
@app.put("/saloes/{salao_id}", response_model=schemas.Salao)
def update_salao(salao_id: int, salao: schemas.SalaoUpdate, db: Session = Depends(get_db)):
    db_salao = crud.get_salao(db, salao_id=salao_id)
    if db_salao is None:
        raise HTTPException(status_code=404, detail="Salão não encontrado")
    return crud.update_salao(db=db, salao_id=salao_id, salao=salao)

# Endpoint para deletar um salão
@app.delete("/saloes/{salao_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_salao(salao_id: int, db: Session = Depends(get_db)):
    db_salao = crud.get_salao(db, salao_id=salao_id)
    if db_salao is None:
        raise HTTPException(status_code=404, detail="Salão não encontrado")
    crud.delete_salao(db=db, salao_id=salao_id)
    return {"detail": "Salão deletado com sucesso"}

#endpoint para criar um profissional
@app.post("/profissionais/", response_model=schemas.Profissional, status_code=status.HTTP_201_CREATED)
def create_profissional(profissional: schemas.ProfissionalCreate, db: Session = Depends(get_db)):
    db_profissional = crud.get_profissional_by_email(db, email=profissional.email)
    if db_profissional:
        raise HTTPException(status_code=400, detail="Email já registrado")
    return crud.create_profissional(db=db, profissional=profissional)

# Endpoint para listar profissionais
@app.get("/profissionais/", response_model=List[schemas.Profissional])
def read_profissionais(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    profissionais = crud.get_profissionais(db, skip=skip, limit=limit)
    return profissionais

# Endpoint para obter um profissional por ID
@app.get("/profissionais/{profissional_id}", response_model=schemas.Profissional)
def read_profissional(profissional_id: int, db: Session = Depends(get_db)):
    db_profissional = crud.get_profissional(db, profissional_id=profissional_id)
    if db_profissional is None:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")
    return db_profissional

# Endpoint para atualizar um profissional
@app.put("/profissionais/{profissional_id}", response_model=schemas.Profissional)
def update_profissional(profissional_id: int, profissional: schemas.ProfissionalUpdate,
                        db: Session = Depends(get_db)):
    db_profissional = crud.get_profissional(db, profissional_id=profissional_id)
    if db_profissional is None:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")
    return crud.update_profissional(db=db, profissional_id=profissional_id, profissional=profissional)

# Endpoint para deletar um profissional
@app.delete("/profissionais/{profissional_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profissional(profissional_id: int, db: Session = Depends(get_db)):
    db_profissional = crud.get_profissional(db, profissional_id=profissional_id)
    if db_profissional is None:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")
    crud.delete_profissional(db=db, profissional_id=profissional_id)
    return {"detail": "Profissional deletado com sucesso"}

# Endpoint para criar um serviço
@app.post("/servicos/", response_model=schemas.Servico, status_code=status.HTTP_201_CREATED)
def create_servico(servico: schemas.ServicoCreate, db: Session = Depends(get_db)):
    return crud.create_servico(db=db, servico=servico)

# Endpoint para listar serviços
@app.get("/servicos/", response_model=List[schemas.Servico])
def read_servicos(skip: int = 0, limit: int = 100, db
: Session = Depends(get_db)):
    servicos = crud.get_servicos(db, skip=skip, limit=limit)
    return servicos

# Endpoint para obter um serviço por ID
@app.get("/servicos/{servico_id}", response_model=schemas.Servico)
def read_servico(servico_id: int, db: Session = Depends(get_db)):
    db_servico = crud.get_servico(db, servico_id=servico_id)
    if db_servico is None:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return db_servico

# Endpoint para atualizar um serviço
@app.put("/servicos/{servico_id}", response_model=schemas.Servico)
def update_servico(servico_id: int, servico: schemas.ServicoUpdate, db
: Session = Depends(get_db)):
    db_servico = crud.get_servico(db, servico_id=servico_id)
    if db_servico is None:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return crud.update_servico(db=db, servico_id=servico_id, servico=servico)

# Endpoint para deletar um serviço
@app.delete("/servicos/{servico_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_servico(servico_id: int, db: Session = Depends(get_db)):
    db_servico = crud.get_servico(db, servico_id=servico_id)
    if db_servico is None:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    crud.delete_servico(db=db, servico_id=servico_id)
    return {"detail": "Serviço deletado com sucesso"}

# Endpoint para criar um cliente
@app.post("/clientes/", response_model=schemas.Cliente, status_code=status.HTTP_201_CREATED)
def create_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    return crud.create_cliente(db=db, cliente=cliente)
# Endpoint para listar clientes
@app.get("/clientes/", response_model=List[schemas.Cliente])
def read_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clientes = crud.get_clientes(db, skip=skip, limit=limit)
    return clientes
# Endpoint para obter um cliente por ID
@app.get("/clientes/{cliente_id}", response_model=schemas.Cliente)
def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = crud.get_cliente(db, cliente_id=cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return db_cliente

# Endpoint para atualizar um cliente
@app.put("/clientes/{cliente_id}", response_model=schemas.Cliente)
def update_cliente(cliente_id: int, cliente: schemas.ClienteUpdate, db: Session = Depends(get_db)):
    db_cliente = crud.get_cliente(db, cliente_id=cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return crud.update_cliente(db=db, cliente_id=cliente_id, cliente=cliente)

# Endpoint para deletar um cliente
@app.delete("/clientes/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = crud.get_cliente(db, cliente_id=cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    crud.delete_cliente(db=db, cliente_id=cliente_id)
    return {"detail": "Cliente deletado com sucesso"}

# Endpoint para criar um agendamento
@app.post("/agendamentos/", response_model=schemas.Agendamento, status_code=status.HTTP_201_CREATED)
def create_agendamento(agendamento: schemas.AgendamentoCreate, db: Session = Depends
(get_db)):
    return crud.create_agendamento(db=db, agendamento=agendamento)

# Endpoint para listar agendamentos
@app.get("/agendamentos/", response_model=List[schemas.Agendamento])
def read_agendamentos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    agendamentos = crud.get_agendamentos(db, skip=skip, limit=limit)
    return agendamentos
# Endpoint para obter um agendamento por ID
@app.get("/agendamentos/{agendamento_id}", response_model=schemas.Agendamento)
def read_agendamento(agendamento_id: int, db: Session = Depends(get_db)):
    db_agendamento = crud.get_agendamento(db, agendamento_id=agendamento_id)
    if db_agendamento is None:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    return db_agendamento
# Endpoint para atualizar um agendamento
@app.put("/agendamentos/{agendamento_id}", response_model=schemas.Agendamento)
def update_agendamento(agendamento_id: int, agendamento: schemas.AgendamentoUpdate
                        , db: Session = Depends(get_db)):
    db_agendamento = crud.get_agendamento(db, agendamento_id=agendamento_id)
    if db_agendamento is None:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    return crud.update_agendamento(db=db, agendamento_id=agendamento_id, agendamento=agendamento)
# Endpoint para deletar um agendamento
@app.delete("/agendamentos/{agendamento_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agendamento(agendamento_id: int, db: Session = Depends(get_db)):
    db_agendamento = crud.get_agendamento(db, agendamento_id=agendamento_id)
    if db_agendamento is None:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    crud.delete_agendamento(db=db, agendamento_id=agendamento_id)
    return {"detail": "Agendamento deletado com sucesso"}

    



