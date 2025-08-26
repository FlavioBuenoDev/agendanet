# backend/tests/test_saloes.py

import pytest # type: ignore
from fastapi.testclient import TestClient
from sqlalchemy import create_engine # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore
from app.main import app
from app.database import Base, get_db
from app.core.security import get_password_hash

# Use um banco de dados de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_create_salao(client: TestClient):
    """
    Testa a criação de um salão.
    """
    salao_data = {
        "nome": "Salão Teste",
        "email": "teste@salao.com",
        "senha": "senhaforte",
        "telefone": "999999999",
        "endereco": "Rua Exemplo, 123",
        "cidade": "Cidade Exemplo",
        "estado": "EX",
        "cep": "12345-678"
    }
    response = client.post("/api/v1/saloes/", json=salao_data)
    assert response.status_code == 201, f"Falha ao criar o salão: {response.text}"
    data = response.json()
    assert "nome" in data
    assert data["nome"] == salao_data["nome"]
    assert "id" in data
    
@pytest.mark.asyncio
async def test_salao_authentication(client: TestClient):
    """
    Testa a autenticação de um salão.
    """
    # Cria um salão para testar a autenticação
    request_data = {
        "nome": "Salão de Autenticação",
        "email": "auth@salao.com",
        "senha": "senhaforte",
        "telefone": "988888888",
        "endereco": "Avenida Teste, 456",
        "cidade": "Cidade Teste",
        "estado": "TS",
        "cep": "87654-321"
    }
    response = client.post("/api/v1/saloes/", json=request_data)
    assert response.status_code == 201, "Falha ao criar salão para autenticação"
    
    # Testa a autenticação
    auth_data = {
        "username": "auth@salao.com",
        "password": "senhaforte"
    }
    response = client.post("/api/v1/token", data=auth_data)
    assert response.status_code == 200, "Falha na autenticação"
    token_data = response.json()
    assert "access_token" in token_data
    assert "token_type" in token_data
