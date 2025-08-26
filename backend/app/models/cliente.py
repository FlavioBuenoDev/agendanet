# backend/app/models/cliente.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey # type: ignore
from sqlalchemy.orm import relationship # type: ignore
from datetime import datetime
from app.database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    senha_hash = Column(String)
    telefone = Column(String)
    criado_em = Column(DateTime, default=datetime.now)
    atualizado_em = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Chave estrangeira para o Salão
    salao_id = Column(Integer, ForeignKey("saloes.id"))
    
    # Relacionamentos
    salao = relationship("Salao", back_populates="clientes")
    agendamentos = relationship("Agendamento", back_populates="cliente")
