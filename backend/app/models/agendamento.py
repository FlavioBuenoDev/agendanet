# backend/app/models/agendamento.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey # type: ignore
from sqlalchemy.orm import relationship # type: ignore
from datetime import datetime
from app.database import Base

class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    data_hora = Column(DateTime)
    criado_em = Column(DateTime, default=datetime.now)
    atualizado_em = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Chaves estrangeiras
    salao_id = Column(Integer, ForeignKey("saloes.id"))
    servico_id = Column(Integer, ForeignKey("servicos.id"))
    profissional_id = Column(Integer, ForeignKey("profissionais.id"))
    cliente_id = Column(Integer, ForeignKey("clientes.id"))

    # Relacionamentos
    salao = relationship("Salao", back_populates="agendamentos")
    servico = relationship("Servico", back_populates="agendamentos")
    profissional = relationship("Profissional", back_populates="agendamentos")
    cliente = relationship("Cliente", back_populates="agendamentos")
