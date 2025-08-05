import pytest # type: ignore
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_client(client: AsyncClient):
    data_cliente = {
        "nome": "Cliente Teste",
        "email": "testecreate@teste.com.br",
        "telefone": "11999999999",
        "senha": "senhateste123"
    }
    response = client.post("/clientes/", json=data_cliente)
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Cliente Teste"
    assert "id" in data
    assert "senha_hash" not in data

# Teste para tentar criar um cliente com e-mail já existente
@pytest.mark.asyncio
async def test_create_existing_client(client: AsyncClient):
    # Primeiro, cria um cliente válido
    data_cliente = {
        "nome": "Cliente Duplicado",
        "email": "teste@teste.com.br",
        "telefone": "11999999999",
        "senha": "senhaduplicada123"
    }
    response = client.post("/clientes/", json=data_cliente)
    assert response.status_code == 201
    # Tenta criar o mesmo cliente novamente
    
    data_cliente = {
        "nome": "Cliente Duplicado2",
        "email": "teste@teste.com.br",
        "telefone": "11999999998", 
        "senha": "senhaduplicada124"
    }
    response = client.post("/clientes/", json=data_cliente)
    assert response.status_code == 400
    assert response.json() == {"detail": "E-mail já cadastrado."}
  
 # Teste para ler um cliente pelo ID   
@pytest.mark.asyncio
async def test_read_client_by_id(client: AsyncClient):
    # 1. Crie um cliente para ser lido
    data_cliente = {
        "nome": "Cliente Leitura",
        "email": "cliente@teste.com.br",
        "telefone": "11888888888",
        "senha": "senhaleitura123"
    }
    response_create = client.post("/clientes/", json=data_cliente)
    # Verifique se a criação foi bem-sucedida
    assert response_create.status_code == 201
    cliente_id = response_create.json()["id"]
    # 2. Leia o cliente pelo ID
    response_read = client.get(f"/clientes/{cliente_id}")
    # 3. Verifique a resposta
    assert response_read.status_code == 200
    data = response_read.json()
    assert data["id"] == cliente_id
    
    

