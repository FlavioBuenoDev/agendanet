# backend/app/models/servico.py

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey # type: ignore
from sqlalchemy.orm import relationship # type: ignore
from datetime import datetime
from app.database import Base

class Servico(Base):
    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(String)
    preco = Column(Float)
    duracao_minutos = Column(Integer)
    criado_em = Column(DateTime, default=datetime.now)
    atualizado_em = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Chave estrangeira para o Salão
    salao_id = Column(Integer, ForeignKey("saloes.id"))
    
    # Relacionamentos
    salao = relationship("Salao", back_populates="servicos")
    agendamentos = relationship("Agendamento", back_populates="servico")
