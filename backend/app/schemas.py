# backend/app/schemas.py
from pydantic import BaseModel, EmailStr, ConfigDict, Field, condecimal
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

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
    nome: str = Field(..., min_length=2, max_length=50)
    especialidade: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    
    model_config = ConfigDict(from_attributes=True)
    
class ProfissionalCreate(ProfissionalBase):
    senha: str = Field(..., min_length=6)
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
    
    model_config = ConfigDict(from_attributes=True)



# --- Esquemas para Serviço ---
class ServicoBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    descricao: Optional[str] = None
    preco: condecimal(max_digits=10, decimal_places=2) = Field(..., ge=0) # type: ignore # Preço com 2 casas decimais e >= 0
    duracao_minutos: int = Field(..., gt=0, description="Duração do serviço em minutos")# Duração em minutos > 0
    
    model_config = ConfigDict(from_attributes=True)

class ServicoCreate(ServicoBase):
    salao_id: int
    
class ServicoUpdate(ServicoBase):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[condecimal(max_digits=10, decimal_places=2)] = None # type: ignore
    duracao_minutos: Optional[int] = None
    is_active: Optional[bool] = None
    
class Servico(ServicoBase):
    id: int
    salao_id: int
    criado_em: datetime
    atualizado_em: datetime
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True) # type: ignore 


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
    senha: str
    pass

class Cliente(ClienteBase):
    id: int
    criado_em: datetime
    atualizado_em: datetime

class ClienteUpdate(ClienteBase):
    senha: Optional[str] = None

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
    
    
# -- Schemas de Autenticação (ADICIONADOS) ---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None

class Login(BaseModel):
    email: str
    senha: str