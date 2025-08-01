# backend/app/models.py

from sqlalchemy import Column, Integer, String, Text, DateTime, DECIMAL, Enum, ForeignKey# type: ignore
from sqlalchemy.orm import relationship # Importe para definir relacionamentos entre tabelas# type: ignore
#from .database import Base # Importa o 'Base' que você definiu em database.py

# backend/app/models.py
#from sqlalchemy.ext.declarative import declarative_base # type: ignore # NOVO: Importe aqui
from sqlalchemy.orm import declarative_base # type: ignore
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text # type: ignore
from sqlalchemy.orm import relationship # type: ignore
from sqlalchemy.sql import func # type: ignore # Para datas automáticas


from datetime import datetime

Base = declarative_base()

class Salao(Base):
    __tablename__ = "saloes" # Define o nome da tabela no banco de dados

    # Definição das colunas da tabela 'saloes'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    endereco = Column(String(255))
    telefone = Column(String(20))
    email = Column(String(255), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    criado_em = Column(DateTime, default=datetime.now)
    atualizado_em = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relacionamentos (opcional, mas muito útil para o ORM)
    # Isso permite que você acesse, por exemplo, 'salao.profissionais'
    profissionais = relationship("Profissional", back_populates="salao")
    servicos = relationship("Servico", back_populates="salao")
    agendamentos = relationship("Agendamento", back_populates="salao")

class Profissional(Base):
    __tablename__ = "profissionais" # Nome da tabela no banco

    id = Column(Integer, primary_key=True, index=True)
    salao_id = Column(Integer, ForeignKey("saloes.id"), nullable=False) # Chave estrangeira
    nome = Column(String(255), nullable=False)
    especialidade = Column(String(100))
    telefone = Column(String(20))
    email = Column(String(255))
    criado_em = Column(DateTime, default=datetime.now)
    atualizado_em = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    salao = relationship("Salao", back_populates="profissionais") # Relacionamento de volta para o Salão
    agendamentos = relationship("Agendamento", back_populates="profissional")

# VOCÊ PRECISA CRIAR AS CLASSES PARA Servico, Cliente e Agendamento AQUI,
# seguindo o mesmo padrão, mapeando as colunas e os relacionamentos.
# Use o script SQL das tabelas como guia para as colunas e tipos de dados.
# Exemplo para Servico:
class Servico(Base):
    __tablename__ = "servicos"
    id = Column(Integer, primary_key=True, index=True)
    salao_id = Column(Integer, ForeignKey("saloes.id"), nullable=False)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text)
    duracao_minutos = Column(Integer, nullable=False)
    preco = Column(DECIMAL(10, 2), nullable=False)
    criado_em = Column(DateTime, default=datetime.now)
    atualizado_em = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    salao = relationship("Salao", back_populates="servicos")
    agendamentos = relationship("Agendamento", back_populates="servico") # Já pensando no relacionamento com Agendamento
    
    
class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    telefone = Column(String(20))
    email = Column(String(255))
    criado_em = Column(DateTime, default=datetime.now)
    atualizado_em = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    agendamentos = relationship("Agendamento", back_populates="cliente")

class Agendamento(Base):
    __tablename__ = "agendamentos"
    id = Column(Integer, primary_key=True, index=True)
    salao_id = Column(Integer, ForeignKey("saloes.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    profissional_id = Column(Integer, ForeignKey("profissionais.id"), nullable=False)
    servico_id = Column(Integer, ForeignKey("servicos.id"), nullable=False)
    data_hora_inicio = Column(DateTime, nullable=False)
    data_hora_fim = Column(DateTime, nullable=False)
    status = Column(Enum('agendado', 'confirmado', 'cancelado', 'concluido'), default='agendado')
    observacoes = Column(Text)
    criado_em = Column(DateTime, default=datetime.now)
    atualizado_em = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relacionamentos
    salao = relationship("Salao", back_populates="agendamentos")
    cliente = relationship("Cliente", back_populates="agendamentos")
    profissional = relationship("Profissional", back_populates="agendamentos")
    servico = relationship("Servico", back_populates="agendamentos")
