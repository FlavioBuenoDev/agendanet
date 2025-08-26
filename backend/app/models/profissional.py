# backend/app/models/profissional.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey # type: ignore
from sqlalchemy.orm import relationship # type: ignore
from datetime import datetime

from app.database import Base # Importação da Base

class Profissional(Base):
    __tablename__ = "profissionais"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    senha_hash = Column(String)
    telefone = Column(String)
    especialidade = Column(String)
    criado_em = Column(DateTime, default=datetime.now)
    atualizado_em = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Chave estrangeira para o Salão
    salao_id = Column(Integer, ForeignKey("saloes.id"))

    # Relacionamento com o Salão
    salao = relationship("Salao", back_populates="profissionais")

    # Relacionamento com Agendamentos
    agendamentos = relationship("Agendamento", back_populates="profissional")
