# backend/app/schemas/servico.py

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# Base Schema para Serviços
class ServicoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    duracao_minutos: int
    
# Schema de criação
class ServicoCreate(ServicoBase):
    pass

# Schema de leitura (retorna dados para o cliente)
class ServicoRead(ServicoBase):
    id: int
    salao_id: int
    criado_em: datetime
    atualizado_em: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Schema de atualização
class ServicoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    duracao_minutos: Optional[int] = None