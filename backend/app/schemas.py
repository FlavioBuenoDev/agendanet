# backend/app/schemas.py
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

# --- Esquemas para Salão ---
class SalaoBase(BaseModel):
    nome: str
    endereco: Optional[str] = None
    telefone: Optional[str] = None
    email: EmailStr
    
    model_config = ConfigDict(from_attributes=True)

class SalaoCreate(SalaoBase):
    senha: str

class Salao(SalaoBase):
    id: int
    criado_em: datetime
    atualizado_em: datetime

class SalaoUpdate(SalaoBase):
    senha: Optional[str] = None

class SalaoDelete(BaseModel):
    id: int
    message: str = "Salão deletado com sucesso"



# --- Esquemas para Profissional ---
class ProfissionalBase(BaseModel):
    nome: str
    especialidade: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    
    model_config = ConfigDict(from_attributes=True)
    
class ProfissionalCreate(ProfissionalBase):
    salao_id: int
    
class ProfissionalUpdate(ProfissionalBase):
    senha: Optional[str] = None
    
class ProfissionalDelete(BaseModel):
    id: int
    message: str = "Profissional deletado com sucesso"
    
class Profissional(ProfissionalBase):
    id: int
    salao_id: int
    criado_em: datetime
    atualizado_em: datetime



# --- Esquemas para Serviço ---
class ServicoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    duracao_minutos: int
    preco: float
    
    model_config = ConfigDict(from_attributes=True)

class ServicoCreate(ServicoBase):
    salao_id: int
    
class Servico(ServicoBase):
    id: int
    salao_id: int
    criado_em: datetime
    atualizado_em: datetime
    
class ServicoUpdate(ServicoBase):
    pass

class ServicoDelete(BaseModel):
    id: int
    message: str = "Serviço deletado com sucesso"



# --- Esquemas para Cliente ---
class ClienteBase(BaseModel):
    nome: str
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    
    model_config = ConfigDict(from_attributes=True)

class ClienteCreate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int
    criado_em: datetime
    atualizado_em: datetime

class ClienteUpdate(ClienteBase):
    pass

class ClienteDelete(BaseModel):
    id: int
    message: str = "Cliente deletado com sucesso"


# --- Esquemas para Agendamento ---
class AgendamentoBase(BaseModel):
    salao_id: int
    cliente_id: int
    profissional_id: int
    servico_id: int
    data_hora_inicio: datetime
    data_hora_fim: datetime
    status: Optional[str] = "agendado"
    observacoes: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class AgendamentoCreate(AgendamentoBase):
    pass

class Agendamento(AgendamentoBase):
    id: int
    criado_em: datetime
    atualizado_em: datetime
    
class AgendamentoUpdate(AgendamentoBase):
    pass

class AgendamentoDelete(BaseModel):
    id: int
    message: str = "Agendamento deletado com sucesso"
    
class AgendamentoList(BaseModel):
    id: int
    cliente_id: int
    profissional_id: int
    servico_id: int
    data_hora_inicio: datetime
    data_hora_fim: datetime
    status: str
    observacoes: Optional[str] = None
    criado_em: datetime
    atualizado_em: datetime

    model_config = ConfigDict(from_attributes=True)