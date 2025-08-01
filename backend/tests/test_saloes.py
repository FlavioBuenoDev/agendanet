# backend/tests/test_saloes.py
import pytest # type: ignore
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_read_root(client: AsyncClient):
    # A chamada ao cliente de teste não precisa de 'await'
    response = client.get("/") 
    assert response.status_code == 200
    assert response.json() == {"message": "Bem-vindo à API de Agendamento do Salão de Beleza!"}

@pytest.mark.asyncio
async def test_create_salao(client: AsyncClient):
    # A chamada ao cliente de teste não precisa de 'await'
    response = client.post(
        "/saloes/",
        json={
            "nome": "Salão Teste Automático",
            "endereco": "Endereço Teste, 456",
            "telefone": "9988776655",
            "email": "teste.auto@example.com",
            "senha": "senhateste123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Salão Teste Automático"
    assert "id" in data
    assert "senha_hash" not in data
    
    
@pytest.mark.asyncio
# Teste para tentar criar um salão com e-mail já existente
async def test_create_existing_salao(client: AsyncClient):
    # Primeiro, cria um salão válido
    response = client.post(
        "/saloes/",
        json={
            "nome": "Salão Duplicado",
            "endereco": "Rua Duplicada, 1",
            "telefone": "1122334455",
            "email": "duplicado@example.com",
            "senha": "senhaunica123"
        }
    )
    assert response.status_code == 201 # Verifica se a primeira criação deu certo
    response = client.post(
        "/saloes/",
        json={
            "nome": "Salão Duplicado",
            "endereco": "Rua Duplicada, 1",
            "telefone": "1122334455",
            "email": "duplicado@example.com",
            "senha": "senhaunica123"
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "E-mail já cadastrado."}


# Teste para ler todos os salões cadastrados    
@pytest.mark.asyncio
async def test_read_saloes(client: AsyncClient):
    client.post(
        "/saloes/",
        json={
            "nome": "Salão de Teste",
            "endereco": "Avenida Teste, 123",
            "telefone": "1234567890",
            "email": "lista@example.com",
            "senha": "senhateste123"
        }
    )
    # A chamada ao cliente de teste não precisa de 'await'
    response = client.get("/saloes/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0   # Verifica se há pelo menos um salão cadastrado
    
# Teste para ler um salão específico pelo ID
@pytest.mark.asyncio
async def test_read_salao_by_id(client: AsyncClient):
    # Primeiro, cria um salão válido
    response = client.post(
        "/saloes/",
        json={
            "nome": "Salão de Teste ID",
            "endereco": "Avenida Teste ID, 123",
            "telefone": "1234567890",
            "email": "id.teste@example.com",
            "senha": "idpass123"
        }
    )
    salao_id = response.json()["id"]
    # A chamada ao cliente de teste não precisa de 'await' 
    response = client.get(f"/saloes/{salao_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == salao_id
    assert data["nome"] == "Salão de Teste ID"
    
# Teste para tentar ler um salão com ID inexistente
@pytest.mark.asyncio
async def test_read_nonexistent_salao(client: AsyncClient):
    # A chamada ao cliente de teste não precisa de 'await'
    response = client.get("/saloes/999999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Salão não encontrado."}
    
# Teste para atualizar um salão existente
@pytest.mark.asyncio
async def test_update_salao(client: AsyncClient):
    # Primeiro, cria um salão válido
    response = client.post(
        "/saloes/",
        json={
            "nome": "Salão Atualizável",
            "endereco": "Avenida Atualização, 123",
            "telefone": "1234567890",
            "email": "test_update@gmail.com",
            "senha": "atualizasenha123"
        }
    )
    salao_id = response.json()["id"]
    # A chamada ao cliente de teste não precisa de 'await'
    response = client.put(
        f"/saloes/{salao_id}",
        json={
            "nome": "Salão Atualizado",
            "endereco": "Avenida Atualização, 456",
            "telefone": "0987654321",
            "email": "test_update@gmail.com",
            "senha": "novasenha123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == salao_id
    assert data["nome"] == "Salão Atualizado"
    assert data["endereco"] == "Avenida Atualização, 456"
    

# TEstes para deletar um salão existente
@pytest.mark.asyncio
async def test_delete_salao(client: AsyncClient):
    # Primeiro, cria um salão válido
    response = client.post(
        "/saloes/",
        json={
            "nome": "Salão para Deletar",
            "endereco": "Rua Deletável, 100",
            "telefone": "9999999999",
            "email": "delete.me@example.com",
            "senha": "deletesenha123"
        }
    )
    salao_id = response.json()["id"]
    # A chamada ao cliente de teste não precisa de 'await'
    response = client.delete(f"/saloes/{salao_id}")
    assert response.status_code == 204
    # Verifica se o salão foi realmente deletado
    response = client.get(f"/saloes/{salao_id}")
    assert response.status_code == 404
    
# Teste para tentar deletar um salão com ID inexistente
@pytest.mark.asyncio
async def test_delete_nonexistent_salao(client: AsyncClient):
    # A chamada ao cliente de teste não precisa de 'await'
    response = client.delete("/saloes/999999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Salão não encontrado."}
    