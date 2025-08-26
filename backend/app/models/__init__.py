# backend/app/models/__init__.py

from .profissional import Profissional # type: ignore # Importa o modelo Profissional
# Você pode adicionar outros modelos aqui no futuro, como:
# from .cliente import Cliente
# from .servico import Servico
from .profissional import Profissional
from .salao import Salao
from .servico import Servico
from .cliente import Cliente
from .agendamento import Agendamento # Importa o novo modelo de Agendamento