# backend/app/main.py

from fastapi import FastAPI
from .database import engine, Base
from .routes import profissionais, saloes, servicos, clientes, agendamentos, auth

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AgendaNet API",
    version="1.0.0",
    description="API para gerenciamento de agendamentos em salões de beleza.",
)

# Inclui as rotas na aplicação
app.include_router(auth.router, prefix="/api/v1")
app.include_router(saloes.router, prefix="/api/v1")
app.include_router(profissionais.router, prefix="/api/v1")
app.include_router(servicos.router, prefix="/api/v1")
app.include_router(clientes.router, prefix="/api/v1")
app.include_router(agendamentos.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API AgendaNet"}