# backend/app/crud.py
from sqlalchemy.orm import Session # type: ignore
from . import models, schemas
from passlib.context import CryptContext # type: ignore # Para hash de senhas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_salao(db: Session, salao_id: int):
    return db.query(models.Salao).filter(models.Salao.id == salao_id).first()

def get_salao_by_email(db: Session, email: str):
    return db.query(models.Salao).filter(models.Salao.email == email).first()

def get_saloes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Salao).offset(skip).limit(limit).all()

def create_salao(db: Session, salao: schemas.SalaoCreate):
    hashed_password = get_password_hash(salao.senha)
    db_salao = models.Salao(
        nome=salao.nome,
        endereco=salao.endereco,
        telefone=salao.telefone,
        email=salao.email,
        senha_hash=hashed_password
    )
    db.add(db_salao)
    db.commit()
    db.refresh(db_salao)
    return db_salao

def update_salao(db: Session, salao_id: int, salao: schemas.SalaoUpdate):
    db_salao = get_salao(db, salao_id)
    if not db_salao:
        return None
    
    if salao.nome:
        db_salao.nome = salao.nome
    if salao.endereco:
        db_salao.endereco = salao.endereco
    if salao.telefone:
        db_salao.telefone = salao.telefone
    if salao.email:
        db_salao.email = salao.email
    if salao.senha:
        db_salao.senha_hash = get_password_hash(salao.senha)
    
    db.commit()
    db.refresh(db_salao)
    return db_salao

def delete_salao(db: Session, salao_id: int):
    db_salao = get_salao(db, salao_id)
    if not db_salao:
        return None
    db.delete(db_salao)
    db.commit()
    return db_salao



############################### PROFISSIONAIS

def get_profissional(db: Session, profissional_id: int):
    return db.query(models.Profissional).filter(models.Profissional.id == profissional_id).first()

def get_profissional_by_email(db: Session, email: str):
    return db.query(models.Profissional).filter(models.Profissional.email == email).first()

def get_profissional_by_salao(db: Session, salao_id: int):
    return db.query(models.Profissional).filter(models.Profissional.salao_id == salao_id).all()

def get_profissionais_by_especialidade(db: Session, especialidade: str):
    return db.query(models.Profissional).filter(models.Profissional.especialidade == especialidade).all()

def get_profissionais_by_salao_and_especialidade(db: Session, salao_id: int, especialidade: str):
    return db.query(models.Profissional).filter(
        models.Profissional.salao_id == salao_id,
        models.Profissional.especialidade == especialidade
    ).all()
    
def get_profissionais_by_nome(db: Session, nome: str):
    return db.query(models.Profissional).filter(models.Profissional.nome.ilike(f"%{nome}%")).all()  

def get_profissionais_by_salao_and_nome(db: Session, salao_id: int, nome: str):
    return db.query(models.Profissional).filter(
        models.Profissional.salao_id == salao_id,
        models.Profissional.nome.ilike(f"%{nome}%")
    ).all() 
    
def get_profissionais_by_salao_and_especialidade_and_nome(db: Session, salao_id: int, especialidade: str, nome: str):
    return db.query(models.Profissional).filter(
        models.Profissional.salao_id == salao_id,
        models.Profissional.especialidade == especialidade,
        models.Profissional.nome.ilike(f"%{nome}%")
    ).all()
    


def get_profissionais(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Profissional).offset(skip).limit(limit).all()

def create_profissional(db: Session, profissional: schemas.ProfissionalCreate):
    db_profissional = models.Profissional(
        salao_id=profissional.salao_id,
        nome=profissional.nome,
        especialidade=profissional.especialidade,
        telefone=profissional.telefone,
        email=profissional.email
    )
    db.add(db_profissional)
    db.commit()
    db.refresh(db_profissional)
    return db_profissional

def update_profissional(db: Session, profissional_id: int, profissional: schemas.ProfissionalUpdate):
    db_profissional = get_profissional(db, profissional_id)
    if not db_profissional:
        return None
    
    if profissional.nome:
        db_profissional.nome = profissional.nome
    if profissional.especialidade:
        db_profissional.especialidade = profissional.especialidade
    if profissional.telefone:
        db_profissional.telefone = profissional.telefone
    if profissional.email:
        db_profissional.email = profissional.email
    
    db.commit()
    db.refresh(db_profissional)
    return db_profissional

def delete_profissional(db: Session, profissional_id: int):
    db_profissional = get_profissional(db, profissional_id)
    if not db_profissional:
        return None
    db.delete(db_profissional)
    db.commit()
    return db_profissional

############################### SERVIÇOS
def get_servico(db: Session, servico_id: int):
    return db.query(models.Servico).filter(models.Servico.id == servico_id).first()
def get_servicos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Servico).offset(skip).limit(limit).all()
def create_servico(db: Session, servico: schemas.ServicoCreate):
    db_servico = models.Servico(
        salao_id=servico.salao_id,
        nome=servico.nome,
        descricao=servico.descricao,
        duracao_minutos=servico.duracao_minutos,
        preco=servico.preco
    )
    db.add(db_servico)
    db.commit()
    db.refresh(db_servico)
    return db_servico
def update_servico(db: Session, servico_id: int, servico: schemas.ServicoUpdate):
    db_servico = get_servico(db, servico_id)
    if not db_servico:
        return None
    
    if servico.nome:
        db_servico.nome = servico.nome
    if servico.descricao:
        db_servico.descricao = servico.descricao
    if servico.duracao_minutos:
        db_servico.duracao_minutos = servico.duracao_minutos
    if servico.preco:
        db_servico.preco = servico.preco
    
    db.commit()
    db.refresh(db_servico)
    return db_servico
def delete_servico(db: Session, servico_id: int):
    db_servico = get_servico(db, servico_id)
    if not db_servico:
        return None
    db.delete(db_servico)
    db.commit()
    return db_servico

############################### CLIENTES
def get_cliente(db: Session, cliente_id: int):
    return db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
def get_clientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Cliente).offset(skip).limit(limit).all()
def create_cliente(db: Session, cliente: schemas.ClienteCreate):
    db_cliente = models.Cliente(
        nome=cliente.nome,
        telefone=cliente.telefone,
        email=cliente.email
    )
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente
def update_cliente(db: Session, cliente_id: int, cliente: schemas.ClienteUpdate):
    db_cliente = get_cliente(db, cliente_id)
    if not db_cliente:
        return None
    
    if cliente.nome:
        db_cliente.nome = cliente.nome
    if cliente.telefone:
        db_cliente.telefone = cliente.telefone
    if cliente.email:
        db_cliente.email = cliente.email
    
    db.commit()
    db.refresh(db_cliente)
    return db_cliente
def delete_cliente(db: Session, cliente_id: int):
    db_cliente = get_cliente(db, cliente_id)
    if not db_cliente:
        return None
    db.delete(db_cliente)
    db.commit()
    return db_cliente

############################### AGENDAMENTOS
def get_agendamento(db: Session, agendamento_id: int):
    return db.query(models.Agendamento).filter(models.Agendamento.id == agendamento_id).first()
def get_agendamentos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Agendamento).offset(skip).limit(limit).all()
def create_agendamento(db: Session, agendamento: schemas.AgendamentoCreate):
    db_agendamento = models.Agendamento(
        salao_id=agendamento.salao_id,
        cliente_id=agendamento.cliente_id,
        profissional_id=agendamento.profissional_id,
        servico_id=agendamento.servico_id,
        data_hora_inicio=agendamento.data_hora_inicio,
        data_hora_fim=agendamento.data_hora_fim,
        status=agendamento.status,
        observacoes=agendamento.observacoes
    )
    db.add(db_agendamento)
    db.commit()
    db.refresh(db_agendamento)
    return db_agendamento
def update_agendamento(db: Session, agendamento_id: int, agendamento: schemas.AgendamentoUpdate):
    db_agendamento = get_agendamento(db, agendamento_id)
    if not db_agendamento:
        return None
    
    if agendamento.profissional_id:
        db_agendamento.profissional_id = agendamento.profissional_id
    if agendamento.servico_id:
        db_agendamento.servico_id = agendamento.servico_id
    if agendamento.cliente_id:
        db_agendamento.cliente_id = agendamento.cliente_id
    if agendamento.data_hora_inicio:
        db_agendamento.data_hora_inicio = agendamento.data_hora_inicio
    if agendamento.data_hora_fim:
        db_agendamento.data_hora_fim = agendamento.data_hora_fim
    if agendamento.status:
        db_agendamento.status = agendamento.status
    if agendamento.observacoes:
        db_agendamento.observacoes = agendamento.observacoes
    
    db.commit()
    db.refresh(db_agendamento)
    return db_agendamento
def delete_agendamento(db: Session, agendamento_id: int):
    db_agendamento = get_agendamento(db, agendamento_id)
    if not db_agendamento:
        return None
    db.delete(db_agendamento)
    db.commit()
    return db_agendamento




# Você também adicionará funções para atualizar e deletar salões,
# e funções CRUD para Profissional, Servico, Cliente e Agendamento.