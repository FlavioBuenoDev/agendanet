# backend/tests/conftest.py
import os
import sys
from pathlib import Path

# Configura o DATABASE_URL para usar um banco de dados SQLite em memória ou em arquivo para testes
# Usar um arquivo (test.db) é geralmente mais fácil para depurar do que :memory:
# Se você quiser um banco de dados temporário que é deletado após o teste, use ':memory:'
# os.environ["DATABASE_URL"] = "sqlite:///:memory:" # Para um banco de dados em memória
os.environ["DATABASE_URL"] = "sqlite:///./test.db" # Para um arquivo de banco de dados temporário

# Adiciona o diretório raiz do projeto ao sys.path para importações absolutas
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest_asyncio # type: ignore
from fastapi.testclient import TestClient # type: ignore
from sqlalchemy import create_engine # type: ignore
from sqlalchemy.orm import sessionmaker, Session # type: ignore

# Importe sua aplicação FastAPI
from app.main import app

# Importe get_db do seu módulo de banco de dados
from app.database import get_db

# Importe a Base e todos os modelos do seu módulo models
# A importação de 'models' garante que todos os modelos declarados na Base sejam registrados.
from app.models import Base
from app import models # Importar o módulo 'models' inteiro é importante!


# Cria um engine para o banco de dados de teste
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest_asyncio.fixture(name="db_session")
async def db_session_fixture():
    """
    Fixture que fornece uma sessão de banco de dados para cada teste,
    garantindo que as tabelas sejam criadas e removidas a cada vez.
    """
    # 1. Cria todas as tabelas (limpa se existirem)
    Base.metadata.drop_all(bind=engine) # Garante que está limpo antes de começar
    Base.metadata.create_all(bind=engine)

    # 2. Cria uma nova sessão de banco de dados para o teste
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    # 3. Sobrescreve a dependência get_db com esta nova sessão
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
            # Note: A transação é revertida na limpeza da fixture 'client'

    app.dependency_overrides[get_db] = override_get_db

    yield session # Fornece a sessão para o teste

    # 4. Limpeza após o teste
    session.close()
    transaction.rollback() # Reverte todas as operações feitas durante o teste
    connection.close()

    # Opcional: Remover o arquivo test.db após todos os testes (se você usou 'sqlite:///./test.db')
    # if os.path.exists("./test.db"):
    #     os.remove("./test.db")


@pytest_asyncio.fixture(name="client")
async def client_fixture(db_session: Session): # Agora, o cliente depende da sessão do DB
    """
    Fixture que fornece um cliente de teste para a aplicação FastAPI.
    Depende de `db_session` para garantir que o banco de dados esteja pronto.
    """
    with TestClient(app) as test_client:
        yield test_client