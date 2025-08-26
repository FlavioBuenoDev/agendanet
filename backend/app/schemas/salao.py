# backend/app/schemas/salao.py

from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

# Base Schema
class SalaoBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: str
    endereco: str
    cidade: str
    estado: str
    cep: str

# Schema de criação (inclui a senha)
class SalaoCreate(SalaoBase):
    senha: str

# Schema de leitura (retorna os dados do salão)
class SalaoRead(SalaoBase):
    id: int
    criado_em: datetime
    atualizado_em: datetime

    model_config = ConfigDict(from_attributes=True)

# Schema de atualização
class SalaoUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
