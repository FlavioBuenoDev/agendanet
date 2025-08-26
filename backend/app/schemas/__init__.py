# backend/app/schemas/__init__.py

from .profissional import ProfissionalCreate, ProfissionalRead, ProfissionalUpdate
from .salao import SalaoCreate, SalaoRead, SalaoUpdate
from .servico import ServicoCreate, ServicoRead, ServicoUpdate
from .cliente import ClienteCreate, ClienteRead, ClienteUpdate
from .agendamento import AgendamentoCreate, AgendamentoRead, AgendamentoUpdate
from .token import Token