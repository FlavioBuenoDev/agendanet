# backend/app/crud.py

from sqlalchemy.orm import Session # type: ignore
from sqlalchemy import func # type: ignore
from typing import List
from datetime import datetime

from app import models, schemas
from app.core.security import get_password_hash # Adicionado para uso na criação de salão e outros

# --- Funções CRUD para Salão ---
def get_salao(db: Session, salao_id: int):
    return db.query(models.Salao).filter(models.Salao.id == salao_id).first()

def get_salao_by_email(db: Session, email: str):
    return db.query(models.Salao).filter(models.Salao.email == email).first()

def get_saloes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Salao).offset(skip).limit(limit).all()

def create_salao(db: Session, salao: schemas.SalaoCreate):
    # A senha já vem hasheada do router
    db_salao = models.Salao(
        nome=salao.nome,
        email=salao.email,
        senha_hash=salao.senha, # A senha já é o hash
        telefone=salao.telefone,
        endereco=salao.endereco,
        cidade=salao.cidade,
        estado=salao.estado,
        cep=salao.cep
    )
    db.add(db_salao)
    db.commit()
    db.refresh(db_salao)
    return db_salao

# --- Funções CRUD para Cliente ---
def get_cliente(db: Session, cliente_id: int):
    return db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()

def get_cliente_by_email(db: Session, email: str):
    return db.query(models.Cliente).filter(models.Cliente.email == email).first()

def get_clientes_by_salao(db: Session, salao_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Cliente).filter(models.Cliente.salao_id == salao_id).offset(skip).limit(limit).all()

# ALTERADO: A função de criação agora recebe e salva o salao_id
def create_cliente(db: Session, cliente: schemas.ClienteCreate, salao_id: int):
    db_cliente = models.Cliente(
        nome=cliente.nome,
        email=cliente.email,
        senha_hash=cliente.senha, # Senha já é o hash
        telefone=cliente.telefone,
        salao_id=salao_id # Salvando o ID do salão
    )
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente
    
def update_cliente(db: Session, cliente_id: int, cliente: schemas.ClienteUpdate):
    db_cliente = get_cliente(db, cliente_id=cliente_id)
    if db_cliente:
        update_data = cliente.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if key == "senha":
                setattr(db_cliente, "senha_hash", get_password_hash(value))
            else:
                setattr(db_cliente, key, value)
        db_cliente.atualizado_em = datetime.now()
        db.commit()
        db.refresh(db_cliente)
    return db_cliente

def delete_cliente(db: Session, cliente_id: int):
    db_cliente = get_cliente(db, cliente_id=cliente_id)
    if db_cliente:
        db.delete(db_cliente)
        db.commit()
    return db_cliente

# --- Funções CRUD para Profissional ---
def get_profissional(db: Session, profissional_id: int):
    return db.query(models.Profissional).filter(models.Profissional.id == profissional_id).first()

def get_profissional_by_email(db: Session, email: str):
    return db.query(models.Profissional).filter(models.Profissional.email == email).first()

def get_profissionais_by_salao(db: Session, salao_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Profissional).filter(models.Profissional.salao_id == salao_id).offset(skip).limit(limit).all()

def create_profissional(db: Session, profissional: schemas.ProfissionalCreate):
    db_profissional = models.Profissional(
        nome=profissional.nome,
        email=profissional.email,
        senha_hash=profissional.senha,
        telefone=profissional.telefone,
        especialidade=profissional.especialidade,
        salao_id=profissional.salao_id
    )
    db.add(db_profissional)
    db.commit()
    db.refresh(db_profissional)
    return db_profissional

def update_profissional(db: Session, profissional_id: int, profissional: schemas.ProfissionalUpdate):
    db_profissional = get_profissional(db, profissional_id=profissional_id)
    if db_profissional:
        update_data = profissional.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if key == "senha":
                setattr(db_profissional, "senha_hash", get_password_hash(value))
            else:
                setattr(db_profissional, key, value)
        db_profissional.atualizado_em = datetime.now()
        db.commit()
        db.refresh(db_profissional)
    return db_profissional

def delete_profissional(db: Session, profissional_id: int):
    db_profissional = get_profissional(db, profissional_id=profissional_id)
    if db_profissional:
        db.delete(db_profissional)
        db.commit()
    return db_profissional

# --- Funções CRUD para Serviço ---
def get_servico_by_id(db: Session, servico_id: int, salao_id: int):
    return db.query(models.Servico).filter(models.Servico.id == servico_id, models.Servico.salao_id == salao_id).first()

def get_servicos_by_salao(db: Session, salao_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Servico).filter(models.Servico.salao_id == salao_id).offset(skip).limit(limit).all()

def create_servico(db: Session, servico: schemas.ServicoCreate, salao_id: int):
    db_servico = models.Servico(**servico.model_dump(), salao_id=salao_id)
    db.add(db_servico)
    db.commit()
    db.refresh(db_servico)
    return db_servico

def update_servico(db: Session, db_servico: models.Servico, servico: schemas.ServicoUpdate):
    update_data = servico.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_servico, key, value)
    db_servico.atualizado_em = datetime.now()
    db.commit()
    db.refresh(db_servico)
    return db_servico

def delete_servico(db: Session, db_servico: models.Servico):
    db.delete(db_servico)
    db.commit()

# --- Funções CRUD para Agendamento ---
def get_agendamento(db: Session, agendamento_id: int):
    return db.query(models.Agendamento).filter(models.Agendamento.id == agendamento_id).first()

def get_agendamentos_by_salao(db: Session, salao_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Agendamento).filter(models.Agendamento.salao_id == salao_id).offset(skip).limit(limit).all()

def create_agendamento(db: Session, agendamento: schemas.AgendamentoCreate, salao_id: int):
    db_agendamento = models.Agendamento(
        data_hora=agendamento.data_hora,
        servico_id=agendamento.servico_id,
        profissional_id=agendamento.profissional_id,
        cliente_id=agendamento.cliente_id,
        salao_id=salao_id
    )
    db.add(db_agendamento)
    db.commit()
    db.refresh(db_agendamento)
    return db_agendamento

def update_agendamento(db: Session, db_agendamento: models.Agendamento, agendamento: schemas.AgendamentoUpdate):
    update_data = agendamento.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_agendamento, key, value)
    db_agendamento.atualizado_em = datetime.now()
    db.commit()
    db.refresh(db_agendamento)
    return db_agendamento

def delete_agendamento(db: Session, agendamento_id: int):
    db_agendamento = get_agendamento(db, agendamento_id)
    if db_agendamento:
        db.delete(db_agendamento)
        db.commit()
    return db_agendamento
