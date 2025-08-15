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
    nome: str = Field(..., min_length=2, max_length=50)
    telefone: Optional[str] = None
    email: EmailStr
    
class ClienteCreate(ClienteBase):
    senha: str = Field(..., min_length=6)

class ClienteUpdate(ClienteBase):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None

class ClienteDelete(BaseModel):
    id: int
    message: str = "Cliente deletado com sucesso"
    

class Cliente(ClienteBase):
    id: int
    is_active: bool
    criado_em: datetime
    atualizado_em: datetime

model_config = ConfigDict(from_attributes=True)


# --- Esquemas para Agendamento ---
# Este esquema representa um agendamento de serviço
class AgendamentoBase(BaseModel):
    data_hora_inicio: datetime # Data e hora de início do agendamento
    data_hora_fim: datetime # Data e hora de fim do agendamento
    status: str = "agendado" # Pode ser 'agendado', 'concluido', 'cancelado'

# Este esquema é usado para criar um novo agendamento
class AgendamentoCreate(AgendamentoBase):
    cliente_id: int
    profissional_id: int
    servico_id: int

# Este esquema representa um agendamento com detalhes adicionais
class Agendamento(AgendamentoBase):
    id: int
    cliente: "Cliente" # Relacionamento aninhado com o schema Cliente
    profissional: "Profissional" # Relacionamento aninhado com o schema Profissional
    servico: "Servico" # Relacionamento aninhado com o schema Servico
  
 # Este esquema é usado para atualizar um agendamento existente   
class AgendamentoUpdate(AgendamentoBase):
    cliente_id: Optional[int] = None
    profissional_id: Optional[int] = None
    servico_id: Optional[int] = None
    status: Optional[str] = None
    data_hora_inicio: Optional[datetime] = None
    data_hora_fim: Optional[datetime] = None
    is_active: Optional[bool] = None
  
# Este esquema é usado para deletar um agendamento  
class AgendamentoDelete(BaseModel):
    id: int
    message: str = "Agendamento deletado com sucesso"
        
    model_config = ConfigDict(from_attributes=True)
    
# Importe as classes aninhadas para evitar erros de referência circular
from .schemas import Cliente, Profissional, Servico
Agendamento.model_rebuild()
    
    
# -- Schemas de Autenticação (ADICIONADOS) ---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None

class Login(BaseModel):
    email: str
    senha: str