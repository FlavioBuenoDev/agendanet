# backend/app/crud.py
import datetime
from sqlalchemy.orm import Session # type: ignore
from . import models, schemas
from passlib.context import CryptContext # type: ignore # Para hash de senhas
from . import models
from sqlalchemy import or_, and_ # type: ignore
from .routes.auth import get_password_hash # type: ignore

# Configuração do passlib para o algoritmo bcryp
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

#def get_password_hash(password: str):
 #   return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


################################ SALÕES

def get_salao(db: Session, salao_id: int):
    return db.query(models.Salao).filter(models.Salao.id == salao_id).first()

def get_salao_by_email(db: Session, email: str):
    return db.query(models.Salao).filter(models.Salao.email == email).first()

def get_saloes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Salao).offset(skip).limit(limit).all()

def create_salao(db: Session, salao: schemas.SalaoCreate):
    senha = get_password_hash(salao.senha) # type: ignore
    db_salao = models.Salao(
        nome=salao.nome,
        endereco=salao.endereco,
        telefone=salao.telefone,
        email=salao.email,
        senha_hash=senha
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
        db_salao.senha_hash = get_password_hash(salao.senha) # type: ignore
    
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
    

# Função para obter todos os profissionais com paginação
def get_profissionais(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Profissional).offset(skip).limit(limit).all()

# Função para criar profissional
def create_profissional(db: Session, profissional: schemas.ProfissionalCreate):
    senha_hash = hash_password(profissional.senha)  
    
    db_profissional = models.Profissional(
        salao_id=profissional.salao_id,
        nome=profissional.nome,
        especialidade=profissional.especialidade,
        telefone=profissional.telefone,
        email=profissional.email,
        senha_hash=senha_hash
    )
    db.add(db_profissional)
    db.commit()
    db.refresh(db_profissional)
    return db_profissional

# Função para atualizar profissional
def update_profissional(db: Session, profissional_id: int, profissional: schemas.ProfissionalUpdate):
    db_profissional = get_profissional(db, profissional_id)
    if not db_profissional:
        return None
    
    update_data = profissional.model_dump(exclude_unset=True)
    
    if "senha" in update_data:
        db_profissional.senha_hash = hash_password(profissional.senha)
        del update_data["senha"]  # Remove senha do update_data
        
    for key, value in update_data.items():
        setattr(db_profissional, key, value)
        
    db.commit()
    db.refresh(db_profissional)
    return db_profissional

def delete_profissional(db: Session, profissional_id: int):
    db_profissional = get_profissional(db, profissional_id)
    if not db_profissional:
        return None
    db.delete(db_profissional)
    db.commit()
    return {"message": "Profissional deletado com sucesso"}

############################### SERVIÇOS
# Funções CRUD para Serviço
def create_servico(db: Session, servico: schemas.ServicoCreate):
    db_servico = models.Servico(
        nome=servico.nome,
        descricao=servico.descricao,
        preco=servico.preco,
        duracao_minutos=servico.duracao_minutos,
        salao_id=servico.salao_id
    )
    db.add(db_servico)
    db.commit()
    db.refresh(db_servico)
    return db_servico

# Funções CRUD para Serviço
def get_servico(db: Session, servico_id: int):
    return db.query(models.Servico).filter(models.Servico.id == servico_id).first()
#  Função para obter todos os serviços de um salão
def get_servicos_by_salao(db: Session, salao_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Servico).filter(models.Servico.salao_id == salao_id).offset(skip).limit(limit).all()

# Função para obter todos os serviços
def update_servico(db: Session, servico_id: int, servico: schemas.ServicoUpdate):
    db_servico = get_servico(db, servico_id=servico_id)
    if db_servico is None:
        return None
        
    update_data = servico.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_servico, key, value)
    
    db.commit()
    db.refresh(db_servico)
    return db_servico
   
# Função para deletar serviço 
def delete_servico(db: Session, servico_id: int):
    db_servico = get_servico(db, servico_id=servico_id)
    if db_servico is None:
        return None
    
    db.delete(db_servico)
    db.commit()
    return {"message": "Serviço deletado com sucesso"}

############################### CLIENTES

# Funções para Clientes
def get_cliente_by_email(db: Session, email: str):
    return db.query(models.Cliente).filter(models.Cliente.email == email).first()

# Função para criar cliente
def create_cliente(db: Session, cliente: schemas.ClienteCreate):
    senha_hash = get_password_hash(cliente.senha)
    db_cliente = models.Cliente(
        nome=cliente.nome,
        telefone=cliente.telefone,
        email=cliente.email,
        senha_hash=senha_hash
    )
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

# Funções CRUD para Cliente
def get_cliente(db: Session, cliente_id: int):
    return db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()

# Função para obter todos os clientes com paginação
def get_clientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Cliente).offset(skip).limit(limit).all()

# Função para atualizar cliente
def update_cliente(db: Session, cliente_id: int, cliente: schemas.ClienteUpdate):
    db_cliente = get_cliente(db, cliente_id=cliente_id)
    if not db_cliente:
        return None
        
    update_data = cliente.model_dump(exclude_unset=True)
    if "senha" in update_data:
        db_cliente.senha_hash = get_password_hash(update_data["senha"])
        del update_data["senha"]

    for key, value in update_data.items():
        setattr(db_cliente, key, value)
    
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

# Função para deletar cliente  
def delete_cliente(db: Session, cliente_id: int):
    db_cliente = get_cliente(db, cliente_id=cliente_id)
    if not db_cliente:
        return None
    db.delete(db_cliente)
    db.commit()
    return {"message": "Cliente deletado com sucesso"}


############################### AGENDAMENTOS
# Funções CRUD para Agendamento

# Função para verificar se o profissional está disponível
def get_agendamentos_by_profissional_and_time(db: Session, profissional_id: int, data_hora_inicio: datetime, data_hora_fim: datetime):
    return db.query(models.Agendamento).filter(
        models.Agendamento.profissional_id == profissional_id,
        models.Agendamento.data_hora_inicio < data_hora_fim,
        models.Agendamento.data_hora_fim > data_hora_inicio
    ).first()

# Função para criar agendamento
def create_agendamento(db: Session, agendamento: schemas.AgendamentoCreate):
    # Lógica para verificar conflito de horário
    conflito = get_agendamentos_by_profissional_and_time(
        db, 
        agendamento.profissional_id,
        agendamento.data_hora_inicio,
        agendamento.data_hora_fim
    )
    if conflito:
        raise ValueError("Profissional não está disponível neste horário.")

    db_agendamento = models.Agendamento(
        cliente_id=agendamento.cliente_id,
        profissional_id=agendamento.profissional_id,
        servico_id=agendamento.servico_id,
        data_hora_inicio=agendamento.data_hora_inicio,
        data_hora_fim=agendamento.data_hora_fim
    )
    db.add(db_agendamento)
    db.commit()
    db.refresh(db_agendamento)
    return db_agendamento

# Função para obter agendamento por ID
def get_agendamento(db: Session, agendamento_id: int):
    return db.query(models.Agendamento).filter(models.Agendamento.id == agendamento_id).first()

# Função para obter todos os agendamentos com paginação
def get_agendamentos_by_cliente(db: Session, cliente_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Agendamento).filter(models.Agendamento.cliente_id == cliente_id).offset(skip).limit(limit).all()

# Função para obter todos os agendamentos de um profissional com paginação
def get_agendamentos_by_profissional(db: Session, profissional_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Agendamento).filter(models.Agendamento.profissional_id == profissional_id).offset(skip).limit(limit).all()

# Função para atualizar agendamento
def delete_agendamento(db: Session, agendamento_id: int):
    db_agendamento = get_agendamento(db, agendamento_id)
    if not db_agendamento:
        return None
    db.delete(db_agendamento)
    db.commit()
    return {"message": "Agendamento deletado com sucesso"}

# ====================================================================
# FUNÇÕES DE AUTENTICAÇÃO
# ====================================================================

def get_user_by_email(db: Session, email: str):
    """
    Função unificada para buscar um usuário por e-mail em todas as tabelas.
    """
    # 1. Tentar encontrar o usuário na tabela Salão
    salao = db.query(models.Salao).filter(models.Salao.email == email).first()
    if salao:
        return salao

    # 2. Se não encontrar, tentar na tabela Profissional
    profissional = db.query(models.Profissional).filter(models.Profissional.email == email).first()
    if profissional:
        return profissional

    # 3. Se ainda não encontrar, tentar na tabela Cliente
    cliente = db.query(models.Cliente).filter(models.Cliente.email == email).first()
    if cliente:
        return cliente

    return None
