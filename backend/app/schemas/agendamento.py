# backend/app/schemas/agendamento.py

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# Base Schema para Agendamentos
class AgendamentoBase(BaseModel):
    data_hora: datetime
    servico_id: int
    profissional_id: int
    cliente_id: int

# Schema de criação
class AgendamentoCreate(AgendamentoBase):
    pass

# Schema de leitura (retorna dados para o cliente)
class AgendamentoRead(AgendamentoBase):
    id: int
    salao_id: int
    criado_em: datetime
    atualizado_em: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Schema de atualização
class AgendamentoUpdate(BaseModel):
    data_hora: Optional[datetime] = None
    servico_id: Optional[int] = None
    profissional_id: Optional[int] = None
    cliente_id: Optional[int] = None
