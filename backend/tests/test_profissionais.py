import pytest # type: ignore
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_profissional(client: AsyncClient):
      # 1. Primeiro, crie um salão para associar o profissional
    salao_data = {
        "nome": "Salão do Profissional",
        "endereco": "Rua do Teste, 101",
        "telefone": "1111111111",
        "email": "salao.profissional@example.com",
        "senha": "senhaprofissional123"
    }
    response_salao = client.post("/saloes/", json=salao_data)
    assert response_salao.status_code == 201
    salao_id = response_salao.json()["id"]
    
    # 2. Agora, crie um profissional associado a esse salão
    profissional_data = {
        "nome": "José Profissional",
        "especialidade": "Cabeleireiro",
        "email": "jose@example.com",
        "salao_id": salao_id
    }
    response_profissional = client.post("/profissionais/", json=profissional_data)
    
    # 3. Verifique a resposta
    assert response_profissional.status_code == 201
    data = response_profissional.json()
    assert data["nome"] == "José Profissional"
    assert "id" in data
    assert data["salao_id"] == salao_id
    assert "senha" not in data # A senha não deve ser retornada
    

@pytest.mark.asyncio
async def test_read_profissional_by_id(client: AsyncClient):
    salao_data = {
        "nome": "Salão Teste Leitura",
        "endereco": "Rua Leitura, 1",
        "telefone": "2222222222",
        "email": "leitura@example.com",
        "senha": "leiturapass123"
    }
    response_salao = client.post("/saloes/", json=salao_data)
    salao_id = response_salao.json()["id"]

    # 2. Cria o profissional que será lido
    profissional_data = {
        "nome": "Ana Leitura",
        "especialidade": "Manicure",
        "email": "ana@example.com",
        "salao_id": salao_id
    }
    response_create = client.post("/profissionais/", json=profissional_data)
    profissional_id = response_create.json()["id"]
    
    # 3. Faz a requisição GET para buscar o profissional por ID
    response_read = client.get(f"/profissionais/{profissional_id}")
    
    # 4. Verifica a resposta
    assert response_read.status_code == 200
    data = response_read.json()
    assert data["id"] == profissional_id
    assert data["nome"] == "Ana Leitura"
    assert data["salao_id"] == salao_id

@pytest.mark.asyncio
async def test_read_profissionais(client: AsyncClient):
    # 1. Cria um salão e um profissional para garantir que a lista não está vazia
    salao_data = {
        "nome": "Salão Lista",
        "endereco": "Rua da Lista, 2",
        "telefone": "3333333333",
        "email": "lista@example.com",
        "senha": "listapass123"
    }
    response_salao = client.post("/saloes/", json=salao_data)
    salao_id = response_salao.json()["id"]
    
    profissional_data = {
        "nome": "Bruno Listagem",
        "especialidade": "Massagista",
        "email": "bruno@example.com",
        "salao_id": salao_id
    }
    client.post("/profissionais/", json=profissional_data)
    
    # 2. Faz a requisição GET para buscar todos os profissionais
    response_list = client.get("/profissionais/")
    
    # 3. Verifica a resposta
    assert response_list.status_code == 200
    data = response_list.json()
    assert isinstance(data, list)
    assert len(data) > 0

@pytest.mark.asyncio
async def test_read_nonexistent_profissional(client: AsyncClient):
    # Tenta ler um profissional com um ID que não existe
    response = client.get("/profissionais/99999999")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Profissional não encontrado."}
    
    
    
# Teste para atualizar um profissional existente
@pytest.mark.asyncio
async def test_update_profissional(client: AsyncClient):
    # 1. Cria um salão
    salao_data = {
        "nome": "Salão para Atualizar Profissional",
        "endereco": "Rua da Atualização, 1",
        "telefone": "4444444444",
        "email": "update.salao@example.com",
        "senha": "updatepass123"
    }
    response_salao = client.post("/saloes/", json=salao_data)
    salao_id = response_salao.json()["id"]

    # 2. Cria o profissional que será atualizado
    profissional_data = {
        "nome": "Carla Atualizável",
        "especialidade": "Esteticista",
        "email": "carla@example.com",
        "salao_id": salao_id
    }
    response_create = client.post("/profissionais/", json=profissional_data)
    profissional_id = response_create.json()["id"]

    # 3. Faz a requisição PUT para atualizar o profissional
    update_data = {
        "nome": "Carla Atualizada",
        "especialidade": "Esteticista e Manicure",
        "email": "carla.nova@example.com",
        "salao_id": salao_id
    }
    response_update = client.put(f"/profissionais/{profissional_id}", json=update_data)

    # 4. Verifica se a atualização foi bem-sucedida
    assert response_update.status_code == 200
    data = response_update.json()
    assert data["nome"] == "Carla Atualizada"
    assert data["especialidade"] == "Esteticista e Manicure"
    assert data["email"] == "carla.nova@example.com"
    
    
# Teste para deletar um profissional existente


@pytest.mark.asyncio
async def test_delete_profissional(client: AsyncClient):
    # 1. Cria um salão
    salao_data = {
        "nome": "Salão para Deletar Profissional",
        "endereco": "Rua da Exclusão, 1",
        "telefone": "5555555555",
        "email": "delete.salao@example.com",
        "senha": "deletepass123"
    }
    response_salao = client.post("/saloes/", json=salao_data)
    salao_id = response_salao.json()["id"]

    # 2. Cria o profissional que será excluído
    profissional_data = {
        "nome": "Daniel Deletável",
        "especialidade": "Cabeleireiro",
        "email": "daniel@example.com",
        "salao_id": salao_id
    }
    response_create = client.post("/profissionais/", json=profissional_data)
    profissional_id = response_create.json()["id"]

    # 3. Faz a requisição DELETE para excluir o profissional
    response_delete = client.delete(f"/profissionais/{profissional_id}")
    
    # 4. Verifica se a exclusão foi bem-sucedida
    assert response_delete.status_code == 200
    assert response_delete.json() == {"message": "Profissional deletado com sucesso."}

    # 5. Tenta ler o profissional excluído para confirmar se ele sumiu
    response_read = client.get(f"/profissionais/{profissional_id}")
    assert response_read.status_code == 404
    assert response_read.json() == {"detail": "Profissional não encontrado."}