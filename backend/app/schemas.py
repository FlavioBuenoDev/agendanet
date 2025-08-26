# backend/app/schemas.py

from pydantic import BaseModel, EmailStr, ConfigDict, Field, condecimal
from typing import Optional, List
from datetime import datetime

# --- Esquemas para Salão ---
class SalaoBase(BaseModel):
    """Esquema base para os dados de salão."""
    nome: str
    endereco: Optional[str] = None
    telefone: Optional[str] = None
    email: EmailStr
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class SalaoCreate(SalaoBase):
    """Esquema para criação de um novo salão. Inclui a senha."""
    senha: str

class Salao(SalaoBase):
    """Esquema de resposta para o salão. Inclui o ID e datas."""
    id: int
    criado_em: datetime
    atualizado_em: datetime

    model_config = ConfigDict(from_attributes=True)

class SalaoUpdate(SalaoBase):
    """Esquema para atualização de um salão. Todos os campos são opcionais."""
    nome: Optional[str] = None
    endereco: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None

class SalaoDelete(BaseModel):
    """Esquema de resposta para exclusão de salão."""
    id: int
    message: str = "Salão deletado com sucesso"


# --- Esquemas para Profissional ---
class ProfissionalBase(BaseModel):
    """Esquema base para os dados de profissional."""
    nome: str = Field(..., min_length=2, max_length=50)
    especialidade: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    
    model_config = ConfigDict(from_attributes=True)
    
class ProfissionalCreate(BaseModel):
    """Esquema para criação de um novo profissional."""
    nome: str
    email: str
    senha: str
    telefone: str
    especialidade: str
    salao_id: int # Campo adicionado para relacionar o profissional ao salão
    
class ProfissionalUpdate(ProfissionalBase):
    """Esquema para atualização de um profissional. Todos os campos são opcionais."""
    senha: Optional[str] = None
    
class ProfissionalDelete(BaseModel):
    """Esquema de resposta para exclusão de profissional."""
    id: int
    message: str = "Profissional deletado com sucesso"
    
class Profissional(ProfissionalBase):
    """Esquema de resposta para o profissional. Inclui ID, salão e datas."""
    id: int
    salao_id: int
    criado_em: datetime
    atualizado_em: datetime
    
    model_config = ConfigDict(from_attributes=True)


# --- Esquemas para Serviço ---
class ServicoBase(BaseModel):
    """Esquema base para os dados de serviço."""
    nome: str = Field(..., min_length=2, max_length=100)
    descricao: Optional[str] = None
    preco: condecimal(max_digits=10, decimal_places=2) = Field(..., ge=0) # type: ignore 
    duracao_minutos: int = Field(..., gt=0, description="Duração do serviço em minutos")
    
    model_config = ConfigDict(from_attributes=True)

class ServicoCreate(ServicoBase):
    """Esquema para criação de um novo serviço."""
    salao_id: int
    
class ServicoUpdate(ServicoBase):
    """Esquema para atualização de um serviço. Todos os campos são opcionais."""
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[condecimal(max_digits=10, decimal_places=2)] = None # type: ignore
    duracao_minutos: Optional[int] = None
    is_active: Optional[bool] = None
    
class Servico(ServicoBase):
    """Esquema de resposta para o serviço."""
    id: int
    salao_id: int
    criado_em: datetime
    atualizado_em: datetime
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True) # type: ignore 


class ServicoDelete(BaseModel):
    """Esquema de resposta para exclusão de serviço."""
    id: int
    message: str = "Serviço deletado com sucesso"


# --- Esquemas para Cliente ---
class ClienteBase(BaseModel):
    """Esquema base para os dados de cliente."""
    nome: str = Field(..., min_length=2, max_length=50)
    telefone: Optional[str] = None
    email: EmailStr
    
    model_config = ConfigDict(from_attributes=True)


class ClienteCreate(ClienteBase):
    """Esquema para criação de um novo cliente. Inclui a senha."""
    senha: str = Field(..., min_length=6)

class ClienteUpdate(ClienteBase):
    """Esquema para atualização de um cliente. Todos os campos são opcionais."""
    nome: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None

class ClienteDelete(BaseModel):
    """Esquema de resposta para exclusão de cliente."""
    id: int
    message: str = "Cliente deletado com sucesso"
    

class Cliente(ClienteBase):
    """Esquema de resposta para o cliente."""
    id: int
    is_active: bool
    criado_em: datetime
    atualizado_em: datetime
    
    model_config = ConfigDict(from_attributes=True)


# --- Esquemas para Agendamento ---
class AgendamentoBase(BaseModel):
    """Esquema base para os dados de agendamento."""
    data_hora_inicio: datetime
    data_hora_fim: datetime
    status: str = "agendado"

class AgendamentoCreate(AgendamentoBase):
    """Esquema para criação de um novo agendamento."""
    cliente_id: int
    profissional_id: int
    servico_id: int

class Agendamento(AgendamentoBase):
    """Esquema de resposta para o agendamento."""
    id: int
    cliente: "Cliente"
    profissional: "Profissional"
    servico: "Servico"
    is_active: bool # Adicionado is_active
    
    model_config = ConfigDict(from_attributes=True)
 
class AgendamentoUpdate(AgendamentoBase):
    """Esquema para atualização de um agendamento. Todos os campos são opcionais."""
    cliente_id: Optional[int] = None
    profissional_id: Optional[int] = None
    servico_id: Optional[int] = None
    status: Optional[str] = None
    data_hora_inicio: Optional[datetime] = None
    data_hora_fim: Optional[datetime] = None
    is_active: Optional[bool] = None

class AgendamentoDelete(BaseModel):
    """Esquema de resposta para exclusão de agendamento."""
    id: int
    message: str = "Agendamento deletado com sucesso"
    
    
# Importe as classes aninhadas para evitar erros de referência circular
# e re-construa o modelo
from .schemas import Cliente, Profissional, Servico
Agendamento.model_rebuild()
    
    
# -- Schemas de Autenticação ---
class Token(BaseModel):
    """Esquema para o token de autenticação."""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Esquema para os dados contidos no token."""
    email: Optional[str] = None

class Login(BaseModel):
    """Esquema para login de usuário."""
    email: str
    senha: str
