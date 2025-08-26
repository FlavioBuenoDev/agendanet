import pytest # type: ignore
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_clientes_crud(client: AsyncClient):
    """
    Testa o fluxo completo de criação, leitura, atualização e exclusão de um cliente,
    incluindo a dependência de um salão.
    """
    # 0. Cria um salão para associar ao cliente
    print("Testando: Criar um Salão para o cliente...")
    salao_data = {
        "nome": "Salão do Cliente",
        "email": "salao.cliente@test.com",
        "senha": "senha-salao",
        "telefone": "11999999999",
        "endereco": "Rua Exemplo, 100",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01000-000"
    }
    response_salao = await client.post("/api/v1/saloes/", json=salao_data)
    assert response_salao.status_code == 201, f"Falha ao criar o salão: {response_salao.text}"
    salao_id = response_salao.json()["id"]

    # Autentica o salão para obter o token de acesso
    print("Testando: Autenticar Salão...") # ALTERADO: Adicionado print para clareza
    auth_salao_response = await client.post(
        # ALTERADO: A rota correta é /api/v1/token, conforme a inclusão no main.py
        "/api/v1/token", 
        data={"username": salao_data["email"], "password": salao_data["senha"]}
    )
    assert auth_salao_response.status_code == 200, f"Falha na autenticação do salão: {auth_salao_response.text}"
    token_data_salao = auth_salao_response.json()
    access_token_salao = token_data_salao["access_token"]
    headers_salao = {"Authorization": f"Bearer {access_token_salao}"}
    
    # 1. Cria um cliente, usando o token do salão
    print("Testando: Criar Cliente...")
    cliente_data = {
        "nome": "Maria do Carmo",
        "email": "maria.carmo@teste.com",
        "senha": "senha-maria",
        "telefone": "11987654321",
    }
    response_create = await client.post("/api/v1/clientes/", json=cliente_data, headers=headers_salao)
    assert response_create.status_code == 201, f"Falha ao criar o cliente: {response_create.text}"
    cliente_id = response_create.json()["id"]

    # 2. Autentica o cliente recém-criado para obter seu próprio token de acesso
    print("Testando: Autenticar Cliente...")
    auth_response = await client.post(
        # ALTERADO: A rota correta é /api/v1/token, conforme a inclusão no main.py
        "/api/v1/token",
        data={"username": cliente_data["email"], "password": cliente_data["senha"]}
    )
    assert auth_response.status_code == 200, f"Falha na autenticação do cliente: {auth_response.text}"
    token_data = auth_response.json()
    access_token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # 3. Lê o cliente recém-criado
    print(f"Testando: Ler Cliente com ID {cliente_id}...")
    response_read_one = await client.get(f"/api/v1/clientes/{cliente_id}", headers=headers_salao) # Use o token do salão para ler o cliente
    assert response_read_one.status_code == 200, f"Falha ao ler o cliente: {response_read_one.text}"
    read_data = response_read_one.json()
    assert read_data["nome"] == "Maria do Carmo"
    assert read_data["email"] == "maria.carmo@teste.com"
    assert read_data["salao_id"] == salao_id

    # 4. Lê o próprio cliente logado através da rota 'me'
    print("Testando: Ler cliente através da rota 'me'...")
    response_read_me = await client.get("/api/v1/clientes/me/", headers=headers)
    assert response_read_me.status_code == 200, f"Falha ao ler o cliente 'me': {response_read_me.text}"
    read_me_data = response_read_me.json()
    assert read_me_data["email"] == "maria.carmo@teste.com"
    assert read_me_data["salao_id"] == salao_id

    # 5. Atualiza o cliente
    print("Testando: Atualizar Cliente...")
    update_data = {
        "nome": "Maria do Carmo Silva",
        "telefone": "11999998888"
    }
    response_update = await client.put(f"/api/v1/clientes/{cliente_id}", json=update_data, headers=headers) # Use o token do cliente para atualizar
    assert response_update.status_code == 200, f"Falha ao atualizar o cliente: {response_update.text}"
    updated_data = response_update.json()
    assert updated_data["nome"] == "Maria do Carmo Silva"
    assert updated_data["telefone"] == "11999998888"
    assert updated_data["email"] == "maria.carmo@teste.com"

    # 6. Exclui o cliente
    print("Testando: Excluir Cliente...")
    response_delete = await client.delete(f"/api/v1/clientes/{cliente_id}", headers=headers) # Use o token do cliente para excluir
    assert response_delete.status_code == 200, f"Falha ao excluir o cliente: {response_delete.text}"
    delete_data = response_delete.json()
    assert delete_data["message"] == "Cliente deletado com sucesso"
    assert delete_data["id"] == cliente_id

    # 7. Tenta ler o cliente excluído (deve falhar)
    print("Testando: Verificar exclusão...")
    response_read_deleted = await client.get(f"/api/v1/clientes/{cliente_id}", headers=headers_salao) # Use o token do salão
    assert response_read_deleted.status_code == 404, f"Cliente não foi excluído corretamente: {response_read_deleted.text}"
    
    print("Sucesso: Todas as etapas do teste de cliente passaram!")
