from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session # type: ignore
from .database import engine, get_db, Base # Importe Base também
from . import models # Importe seus modelos

# Base.metadata.create_all(bind=engine) # Não use isso com Alembic em produção, apenas para testes rápidos sem migrações!

app = FastAPI(
    title="API de Agendamento Salão de Beleza",
    description="API para gerenciar agendamentos, salões, profissionais, serviços e clientes.",
    version="0.1.0",
)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Agendamento do Salão de Beleza!"}

# Exemplo simples: criar um endpoint para listar salões
# Você vai precisar criar schemas.py e crud.py para isso funcionar corretamente mais tarde
# Mas para testar a conexão, podemos fazer algo básico:
@app.get("/saloes/")
def get_saloes(db: Session = Depends(get_db)):
    # Isso vai falhar se a tabela estiver vazia, mas serve para testar a conexão
    return db.query(models.Salao).all()