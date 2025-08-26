# backend/app/schemas/profissional.py

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# Base Schema (compartilhado por todos os outros schemas)
class ProfissionalBase(BaseModel):
    nome: str
    email: str
    telefone: str
    especialidade: str

# Schema de criação (recebe dados do cliente, incluindo a senha)
class ProfissionalCreate(ProfissionalBase):
    senha: str

# Schema de leitura (retorna dados para o cliente)
class ProfissionalRead(ProfissionalBase):
    id: int
    salao_id: int
    criado_em: datetime
    atualizado_em: datetime

    model_config = ConfigDict(from_attributes=True)

# Schema de atualização (usado para atualizar informações existentes)
class ProfissionalUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None
    telefone: Optional[str] = None
    especialidade: Optional[str] = None
