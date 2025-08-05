# backend/tests/test_saloes.py
import pytest # type: ignore
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_servico(client: AsyncClient):
    # 1. Crie um salão para associar o serviço
    salao_data = {
        "nome": "Salão dos Serviços",
        "endereco": "Rua do Serviço, 101",
        "telefone": "1111111111",
        "email": "servico.salao@example.com",
        "senha": "senhaservico123"
    }
    response_salao = client.post("/saloes/", json=salao_data)
    assert response_salao.status_code == 201
    salao_id = response_salao.json()["id"]

    # 2. Crie um serviço associado a esse salão
    servico_data = {
        "nome": "Corte de Cabelo",
        "descricao": "Corte moderno para qualquer estilo.",
        "duracao_minutos": 45,
        "preco": 60.00,
        "salao_id": salao_id
    }
    response_servico = client.post("/servicos/", json=servico_data)
    
    # 3. Verifique a resposta
    assert response_servico.status_code == 201
    data = response_servico.json()
    assert data["nome"] == "Corte de Cabelo"
    assert "id" in data
    assert data["salao_id"] == salao_id
    assert data["preco"] == 60.00
    
    
@pytest.mark.asyncio
async def test_read_servico_by_id(client: AsyncClient):
    # 1. Crie um salão e um serviço para ser lido
    salao_data = {
        "nome": "Salão de Teste Leitura Serviço",
        "endereco": "Rua da Leitura, 123",
        "telefone": "2222222222",
        "email": "leitura.servico@example.com",
        "senha": "leiturapass123"
    }
    response_salao = client.post("/saloes/", json=salao_data)
    salao_id = response_salao.json()["id"]

    servico_data = {
        "nome": "Manicure e Pedicure",
        "descricao": "Serviço de unhas completo.",
        "duracao_minutos": 60,
        "preco": 45.00,
        "salao_id": salao_id
    }
    response_create = client.post("/servicos/", json=servico_data)
    servico_id = response_create.json()["id"]

    # 2. Faça a requisição GET para buscar o serviço pelo ID
    response_read = client.get(f"/servicos/{servico_id}")
    
    # 3. Verifique a resposta
    assert response_read.status_code == 200
    data = response_read.json()
    assert data["id"] == servico_id
    assert data["nome"] == "Manicure e Pedicure"
    assert data["salao_id"] == salao_id

# Teste para tentar criar um serviço com salão inexistente
@pytest.mark.asyncio
async def test_read_servicos(client: AsyncClient):
    # 1. Crie um salão e um serviço para garantir que a lista não está vazia
    salao_data = {
        "nome": "Salão Lista Serviços",
        "endereco": "Rua da Lista, 456",
        "telefone": "3333333333",
        "email": "lista.servico@example.com",
        "senha": "listapass123"
    }
    response_salao = client.post("/saloes/", json=salao_data)
    salao_id = response_salao.json()["id"]
    
    servico_data = {
        "nome": "Hidratação Capilar",
        "descricao": "Tratamento para cabelos ressecados.",
        "duracao_minutos": 30,
        "preco": 80.00,
        "salao_id": salao_id
    }
    client.post("/servicos/", json=servico_data)
    
    # 2. Faça a requisição GET para buscar todos os serviços
    response_list = client.get("/servicos/")
    
    # 3. Verifique a resposta
    assert response_list.status_code == 200
    data = response_list.json()
    assert isinstance(data, list)
    assert len(data) > 0

@pytest.mark.asyncio
async def test_read_nonexistent_servico(client: AsyncClient):
    # Tente ler um serviço com um ID que não existe
    response = client.get("/servicos/99999999")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Serviço não encontrado."}
    
    

# Teste para atualizar um serviço existente
@pytest.mark.asyncio
async def test_update_servico(client: AsyncClient):
    # 1. Crie um salão e um serviço que será atualizado
    salao_data = {
        "nome": "Salão Atualização Serviço",
        "endereco": "Rua da Atualização, 123",
        "telefone": "4444444444",
        "email": "update.servico@example.com",
        "senha": "updatepass123"
    }
    response_salao = client.post("/saloes/", json=salao_data)
    salao_id = response_salao.json()["id"]
    

    servico_data = {
        "nome": "Corte Feminino",
        "descricao": "Corte de cabelo padrão.",
        "duracao_minutos": 45,
        "preco": 50.00,
        "salao_id": salao_id
    }
    response_create = client.post("/servicos/", json=servico_data)
    servico_id = response_create.json()["id"]
    

    # 2. Faça a requisição PUT para atualizar o serviço
    update_data = {
        "nome": "Corte Feminino (Upgrade)",
        "descricao": "Corte de cabelo com lavagem e secagem.",
        "duracao_minutos": 60,
        "preco": 75.00,
        "salao_id": salao_id
    }
    response_update = client.put(f"/servicos/{servico_id}", json=update_data)

    # 3. Verifique se a atualização foi bem-sucedida
    assert response_update.status_code == 200
    data = response_update.json()
    assert data["nome"] == "Corte Feminino (Upgrade)"
    assert data["preco"] == 75.00
    assert response_update.json() == {"message": "Serviço atualizado com sucesso."}
    
    
# Teste para excluir um serviço existente    
@pytest.mark.asyncio
async def test_delete_servico(client: AsyncClient):
    # 1. Crie um salão e um serviço que será excluído
    salao_data = {
        "nome": "Salão Exclusão Serviço",
        "endereco": "Rua da Exclusão, 123",
        "telefone": "5555555555",
        "email": "delete.servico@example.com",
        "senha": "deletepass123"
    }
    response_salao = client.post("/saloes/", json=salao_data)
    salao_id = response_salao.json()["id"]

    servico_data = {
        "nome": "Serviço a Ser Deletado",
        "descricao": "Este serviço será removido.",
        "duracao_minutos": 30,
        "preco": 30.00,
        "salao_id": salao_id
    }
    response_create = client.post("/servicos/", json=servico_data)
    servico_id = response_create.json()["id"]

    # 2. Faça a requisição DELETE para excluir o serviço
    response_delete = client.delete(f"/servicos/{servico_id}")
    
    # 3. Verifique se a exclusão foi bem-sucedida
    assert response_delete.status_code == 200
    assert response_delete.json() == {"message": "Serviço deletado com sucesso."}

    # 4. Tente ler o serviço excluído para confirmar se ele sumiu
    response_read = client.get(f"/servicos/{servico_id}")
    assert response_read.status_code == 404
    assert response_read.json() == {"detail": "Serviço não encontrado."}