from sqlalchemy import Column, Integer, String, DateTime, ForeignKey # type: ignore
from sqlalchemy.orm import relationship # type: ignore
from datetime import datetime
from app.database import Base

class Salao(Base):
    __tablename__ = "saloes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    senha_hash = Column(String)
    telefone = Column(String)
    endereco = Column(String)
    cidade = Column(String)
    estado = Column(String)
    cep = Column(String)
    criado_em = Column(DateTime, default=datetime.now)
    atualizado_em = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relacionamento com Profissionais, Clientes, Agendamentos e Serviços
    profissionais = relationship("Profissional", back_populates="salao")
    clientes = relationship("Cliente", back_populates="salao")
    agendamentos = relationship("Agendamento", back_populates="salao")
    servicos = relationship("Servico", back_populates="salao")