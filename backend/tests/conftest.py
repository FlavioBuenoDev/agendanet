# backend/tests/conftest.py
import os
import sys
from pathlib import Path
from typing import AsyncGenerator


# Adiciona o diretório raiz do projeto ao sys.path para importações absolutas
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest_asyncio # type: ignore
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore

from app.main import app
from app.database import Base, get_db

# Configurações do banco de dados de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest_asyncio.fixture(scope="function")
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    Fixtura assíncrona que fornece um cliente de teste para a aplicação FastAPI.
    Cria e limpa o banco de dados para CADA FUNÇÃO de teste.
    """
    # 1. Cria o banco de dados de teste
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # Adicione esta linha para ver as consultas SQL (DEBUG)
    engine.echo = True

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    # 2. Limpa o banco de dados após a execução dos testes
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    os.remove("./test.db") if os.path.exists("./test.db") else None