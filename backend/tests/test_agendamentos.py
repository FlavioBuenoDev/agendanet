# backend/tests/test_agendamentos.py
import pytest # type: ignore
from httpx import AsyncClient
from datetime import datetime, timedelta

'''
@pytest.mark.asyncio
async def test_create_agendamento(client: AsyncClient):
    # 1. Pré-condições: Crie um salão, cliente, profissional e serviço
    salao_data = {"nome": "Salão do Agendamento", "endereco": "Rua Agendamento, 123", "telefone": "1111111111", "email": "agenda@example.com", "senha": "senhatest"}
    response_salao = client.post("/saloes/", json=salao_data)
    salao_id = response_salao.json()["id"]

    cliente_data = {"nome": "Cliente Teste", "email": "cliente@example.com", "telefone": "2222222222", "senha": "clientesenha"}
    response_cliente = client.post("/clientes/", json=cliente_data)
    cliente_id = response_cliente.json()["id"]

    profissional_data = {"nome": "Profissional Teste", "especialidade": "Cabeleireiro", "email": "profissional@example.com", "salao_id": salao_id}
    response_profissional = client.post("/profissionais/", json=profissional_data)
    profissional_id = response_profissional.json()["id"]
    
    servico_data = {"nome": "Corte Simples", "descricao": "Corte de cabelo rápido", "duracao_minutos": 30, "preco": 50.0, "salao_id": salao_id}
    response_servico = client.post("/servicos/", json=servico_data)
    servico_id = response_servico.json()["id"]

    # extrair a duração do serviço para usar no cálculo
    servico_duracao = response_servico.json()["duracao_minutos"]

    # 2. Dados do agendamento
    data_hora_inicio_objeto = datetime.now() + timedelta(days=1)
    # data_hora_inicio = datetime.now() + timedelta(days=1)
    
    # Adicione a lógica para calcular a data_hora_fim
    data_hora_fim_objeto = data_hora_inicio_objeto + timedelta(minutes=servico_duracao)

    agendamento_data = {
        "data_hora_inicio": data_hora_inicio_objeto.isoformat(),
        "data_hora_fim": data_hora_fim_objeto.isoformat(),
        "cliente_id": cliente_id,
        "profissional_id": profissional_id,
        "servico_id": servico_id,
        "salao_id": salao_id
    }

    # 3. Faz a requisição POST para criar o agendamento
    response_agendamento = client.post("/agendamentos/", json=agendamento_data)
    
    # 4. Verifique a resposta
    assert response_agendamento.status_code == 201
    data = response_agendamento.json()
    assert "id" in data
    assert data["cliente_id"] == cliente_id
    assert data["profissional_id"] == profissional_id
    assert data["servico_id"] == servico_id
    
'''
#Agendamento de Conflitos Teste
@pytest.mark.asyncio
async def test_create_agendamento_conflito(client: AsyncClient):
    # 1. Pré-condições: Crie todas as entidades necessárias
    salao_data = {"nome": "Salão do Conflito", "endereco": "Rua Conflito, 456", "telefone": "3333333333", "email": "conflito@example.com", "senha": "senhatest"}
    response_salao = await client.post("/saloes/", json=salao_data)
    salao_id = response_salao.json()["id"]

    cliente_data = {"nome": "Cliente Conflito", "email": "cliente2@example.com", "telefone": "4444444444", "senha": "clientesenha2"}
    response_cliente = await  client.post("/clientes/", json=cliente_data)
    cliente_id = response_cliente.json()["id"]

    profissional_data = {"nome": "Profissional Conflito", "especialidade": "Manicure", "email": "profissional2@example.com", "salao_id": salao_id}
    response_profissional = await client.post("/profissionais/", json=profissional_data)
    profissional_id = response_profissional.json()["id"]

    servico_data = {"nome": "Manicure Simples", "descricao": "Serviço de unhas", "duracao_minutos": 45, "preco": 30.0, "salao_id": salao_id}
    response_servico = await client.post("/servicos/", json=servico_data)
    servico_id = response_servico.json()["id"]

    # 2. Crie o primeiro agendamento com sucesso
    # CHAVE: Armazena o datetime.now() em uma variável para ser exatamente o mesmo
    data_hora_inicio_do_teste = datetime.now() + timedelta(days=2) 
    servico_duracao = response_servico.json()["duracao_minutos"]
    data_hora_fim_do_teste = data_hora_inicio_do_teste + timedelta(minutes=servico_duracao)

    agendamento_data = {
        "data_hora_inicio": data_hora_inicio_do_teste.isoformat(),
        "data_hora_fim": data_hora_fim_do_teste.isoformat(),
        "cliente_id": cliente_id,
        "profissional_id": profissional_id,
        "servico_id": servico_id,
        "salao_id": salao_id
    }

    response_primeiro_agendamento = await client.post("/agendamentos/", json=agendamento_data)
    assert response_primeiro_agendamento.status_code == 201

    # 3. Tente criar um segundo agendamento com conflito de horário
    # Usando os mesmos dados e o mesmo profissional, no mesmo horário
    response_segundo_agendamento = await client.post("/agendamentos/", json=agendamento_data)

    # 4. Verifique se a API retorna um erro 400
    assert response_segundo_agendamento.status_code == 400