# API de Agendamento para Salão de Beleza

Bem-vindo à API de Agendamento do Salão de Beleza. Esta API RESTful foi desenvolvida com FastAPI e SQLAlchemy para gerenciar agendamentos, clientes, profissionais, serviços e salões de beleza de forma eficiente.

## 🚀 Funcionalidades

- **CRUD Completo:** Gerenciamento completo de Salões, Clientes, Profissionais, Serviços e Agendamentos.
- **Validação de Negócios:**
    - Verificação de e-mail único para Salões e Profissionais.
    - Validação de conflito de horário para agendamentos, garantindo que um profissional não seja agendado para dois serviços ao mesmo tempo.
- **Estrutura Organizada:** O código-fonte é modular e refatorado, com rotas separadas por entidade para facilitar a manutenção e o crescimento.
- **Testes Automatizados:** Testes unitários e de integração com Pytest para garantir o funcionamento correto da API.

---

## 🛠️ Tecnologias

- **Framework:** FastAPI
- **Banco de Dados:** SQLite (com SQLAlchemy ORM)
- **Hasing de Senhas:** passlib
- **Validação:** Pydantic
- **Testes:** Pytest

---

## ⚙️ Como Começar

Siga estas instruções para configurar e rodar o projeto localmente.

### Pré-requisitos

Certifique-se de ter o Python 3.8+ e o `pip` instalados na sua máquina.

### Instalação

1.  Clone o repositório:
    ```bash
    git clone [https://github.com/seu-usuario/seu-projeto.git](https://github.com/seu-usuario/seu-projeto.git)
    cd seu-projeto
    ```
2.  Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate
    # No macOS/Linux:
    source venv/bin/activate
    ```
3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
    *(Nota: Certifique-se de ter um arquivo `requirements.txt` com todas as bibliotecas usadas ou execute `pip install -r requirements.txt`)*

### Rodando a Aplicação

Para iniciar o servidor com o Uvicorn, execute o seguinte comando na raiz do projeto:

```bash
uvicorn app.main:app --reload



A API estará disponível em http://127.0.0.1:8000.

🗺️ Endpoints da API
A documentação interativa (Swagger UI) pode ser acessada em http://127.0.0.1:8000/docs.

Entidades
/saloes/

/profissionais/

/servicos/

/clientes/

/agendamentos/

✒️ Autor
Flávio Bueno
Luan Marques
