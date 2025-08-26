# backend/app/schemas/cliente.py

from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

# Base Schema para Clientes
class ClienteBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: str

# Schema de criação
class ClienteCreate(ClienteBase):
    senha: str
    salao_id: Optional[int] = None

# Schema de leitura (retorna dados para o cliente)
class ClienteRead(ClienteBase):
    id: int
    salao_id: int
    criado_em: datetime
    atualizado_em: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Schema de atualização
class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    telefone: Optional[str] = None