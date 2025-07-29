# backend/app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# Define os esquemas Pydantic para validação e serialização de dados

# Classe Salao
class SalaoBase(BaseModel):
    nome: str
    endereco: Optional[str] = None
    telefone: Optional[str] = None
    email: EmailStr # Usa EmailStr para validação de formato de e-mail

class SalaoCreate(SalaoBase):
    senha: str # A senha será enviada na criação, mas não retornada

class Salao(SalaoBase):
    id: int
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        orm_mode = True # Importante para que o Pydantic possa ler dados de modelos SQLAlchemy
    
class SalaoUpdate(SalaoBase):
    senha: Optional[str] = None # Permite atualizar o salão sem precisar enviar a senha novamente

class SalaoDelete(BaseModel):
    id: int
    message: str = "Salão deletado com sucesso"
    
            
# Classe Profissional
class ProfissionalBase(BaseModel):
    nome: str
    especialidade: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    
class ProfissionalCreate(ProfissionalBase):
    salao_id: int # Necessário para criar um profissional associado a um salão
    
class ProfissionalUpdate(ProfissionalBase):
    senha: Optional[str] = None # Permite atualizar o profissional sem precisar enviar a senha novamente
    
class ProfissionalDelete(BaseModel):
    id: int
    message: str = "Profissional deletado com sucesso"
    
class Profissional(ProfissionalBase):
    id: int
    salao_id: int
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        orm_mode = True # Permite que o Pydantic leia dados de modelos SQLAlchemy

class Profissional(ProfissionalBase):
    id: int
    salao_id: int
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        orm_mode = True # Permite que o Pydantic leia dados de modelos SQLAlchemy
 
       
# Classe Servico
class ServicoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    duracao_minutos: int
    preco: float # Usando float para representar valores monetários
    
class ServicoCreate(ServicoBase):
    salao_id: int # Necessário para criar um serviço associado a um salão
    
class Servico(ServicoBase):
    id: int
    salao_id: int
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        orm_mode = True # Permite que o Pydantic leia dados de modelos SQLAlchemy
   
class ServicoUpdate(ServicoBase):
    pass # Pode ser estendido se necessário
    
# Classe ServicoDelete
class ServicoDelete(BaseModel):
    id: int
    message: str = "Serviço deletado com sucesso"

        
# Classe Cliente
class ClienteBase(BaseModel):
    nome: str
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    
class ClienteCreate(ClienteBase):
    pass # Pode ser estendido se necessário

class Cliente(ClienteBase):
    id: int
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        orm_mode = True # Permite que o Pydantic leia dados de modelos SQLAlchemy   

class ClienteUpdate(ClienteBase):
    pass # Pode ser estendido se necessário

class ClienteDelete(BaseModel):
    id: int
    message: str = "Cliente deletado com sucesso" 
 

# Schema Base para Agendamento - contém os campos comuns
class AgendamentoBase(BaseModel):
    salao_id: int
    cliente_id: int
    profissional_id: int
    servico_id: int
    # Inclua data_hora_inicio e data_hora_fim aqui
    data_hora_inicio: datetime # Deve corresponder ao tipo do seu modelo
    data_hora_fim: datetime   # Deve corresponder ao tipo do seu modelo
    status: Optional[str] = "agendado" # Status pode ser opcional com um valor padrão
    observacoes: Optional[str] = None

# Schema para Criação - herda do Base
class AgendamentoCreate(AgendamentoBase):
    pass # No seu caso, pode herdar diretamente ou adicionar campos específicos se houver

# Schema para Leitura - herda do Base e adiciona campos gerados pelo DB
class Agendamento(AgendamentoBase):
    id: int
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        orm_mode = True # Permite que o Pydantic leia dados de modelos SQLAlchemy
        
# Schema para Atualização - herda do Base
class AgendamentoUpdate(AgendamentoBase):
    pass # Pode ser estendido se necessário

# Schema para Exclusão
class AgendamentoDelete(BaseModel):
    id: int
    message: str = "Agendamento deletado com sucesso"
    
# Schema para Listagem de Agendamentos
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

    class Config:
        orm_mode = True # Permite que o Pydantic leia dados de modelos SQLAlchemy
        