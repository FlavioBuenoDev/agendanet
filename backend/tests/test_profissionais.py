# backend/tests/test_profissionais.py

import pytest # type: ignore
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_profissionais_crud(client: AsyncClient):
    """
    Testa o fluxo completo de criação, leitura, atualização e exclusão de um profissional.
    """
    # 1. Cria um salão para autenticação
    print("Testando: Criar Salão para autenticação...")
    salao_data = {
        "nome": "Salão do Zé",
        "email": "salao.ze@email.com",
        "senha": "senha-segura",
        "telefone": "11987654321",
        "endereco": "Rua das Flores, 100",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01000-000"
    }
    # Corrigido para incluir o prefixo da API
    response_salao = await client.post("/api/v1/saloes/", json=salao_data)
    assert response_salao.status_code == 201, f"Falha ao criar o salão: {response_salao.text}"

    # 2. Autentica o salão para obter um token de acesso
    print("Testando: Autenticar Salão...")
    auth_response = await client.post(
        "/api/v1/auth/token", 
        data={"username": salao_data["email"], "password": salao_data["senha"]}
    )
    assert auth_response.status_code == 200, f"Falha na autenticação do salão: {auth_response.text}"
    token_data = auth_response.json()
    access_token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Obtém o ID do salão criado
    salao_id = response_salao.json()["id"]

    # 3. Cria um profissional
    print("Testando: Criar Profissional...")
    profissional_data = {
        "nome": "João da Silva",
        "email": "joao.silva@teste.com",
        "senha": "senha-joao",
        "telefone": "11999999999",
        "especialidade": "Corte de Cabelo",
        "salao_id": salao_id # Garante que o ID do salão está correto
    }
    # Corrigido para incluir o prefixo da API
    response_create = await client.post("/api/v1/profissionais/", json=profissional_data, headers=headers)
    assert response_create.status_code == 201, f"Falha ao criar o profissional: {response_create.text}"
    new_profissional = response_create.json()
    assert new_profissional["nome"] == profissional_data["nome"]
    
    # 4. Lê o profissional recém-criado
    print("Testando: Ler Profissional...")
    profissional_id = new_profissional["id"]
    # Corrigido para incluir o prefixo da API
    response_get = await client.get(f"/api/v1/profissionais/{profissional_id}", headers=headers)
    assert response_get.status_code == 200, f"Falha ao ler o profissional: {response_get.text}"
    assert response_get.json()["id"] == profissional_id
    
    # 5. Lê todos os profissionais
    print("Testando: Ler todos os Profissionais...")
    response_read_all = await client.get("/api/v1/profissionais/", headers=headers)
    assert response_read_all.status_code == 200, f"Falha ao ler todos os profissionais: {response_read_all.text}"
    all_profissionais = response_read_all.json()
    assert len(all_profissionais) == 1
    assert all_profissionais[0]["id"] == profissional_id
    
    
    # 6. Atualiza o profissional
    print("Testando: Atualizar Profissional...")
    update_data = {
        "nome": "João Silva Júnior",
        "telefone": "11988888888",
        "especialidade": "Corte e Cor"
    }
    # Corrigido para incluir o prefixo da API
    response_update = await client.put(f"/api/v1/profissionais/{profissional_id}", json=update_data, headers=headers)
    assert response_update.status_code == 200, f"Falha ao atualizar o profissional: {response_update.text}"
    updated_profissional = response_update.json()
    assert updated_profissional["nome"] == update_data["nome"]
    assert updated_profissional["telefone"] == update_data["telefone"]
    assert updated_profissional["especialidade"] == update_data["especialidade"]
    
    # 6. Lê todos os profissionais para verificar se o novo está na lista
    print("Testando: Ler todos os Profissionais...")
    # Corrigido para incluir o prefixo da API
    response_get_all = await client.get("/api/v1/profissionais/", headers=headers)
    assert response_get_all.status_code == 200, f"Falha ao ler todos os profissionais: {response_get_all.text}"
    all_profissionais = response_get_all.json()
    assert any(p["id"] == profissional_id for p in all_profissionais)

    # 7. Exclui o profissional
    print("Testando: Deletar Profissional...")
    # Corrigido para incluir o prefixo da API
    response_delete = await client.delete(f"/api/v1/profissionais/{profissional_id}", headers=headers)
    assert response_delete.status_code == 200, f"Falha ao deletar o profissional: {response_delete.text}"
    assert "Profissional deletado com sucesso" in response_delete.json()["message"]
    
    # 8. Tenta ler o profissional excluído para confirmar que ele não existe mais
    print("Testando: Confirmar deleção...")
    # Corrigido para incluir o prefixo da API
    response_get_deleted = await client.get(f"/api/v1/profissionais/{profissional_id}", headers=headers)
    assert response_get_deleted.status_code == 404, "Profissional não foi deletado, ainda está acessível."

    print("Todos os testes de CRUD de profissionais foram bem-sucedidos!")
