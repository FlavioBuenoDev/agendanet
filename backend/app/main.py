# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError # type: ignore
from sqlalchemy.orm import Session # type: ignore
from typing import List
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine # type: ignore
from sqlalchemy.orm import sessionmaker, Session # type: ignore
from contextlib import contextmanager
from .database import Base, get_db
from .routes import profissionais, saloes, servicos, clientes, agendamentos, auth

from .database import get_db
from . import models, schemas, crud # Importação do crud e os schemas

''''
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
'''
        
app = FastAPI(
    title="API de Agendamento Salão de Beleza",
    description="API para gerenciar agendamentos, salões, profissionais, serviços e clientes.",
    version="0.1.0",
)

# Manipulador global para IntegrityError
@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "E-mail já cadastrado."}
    )


@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Agendamento do Salão de Beleza!"}


######################### SALÕES #########################

app.include_router(saloes.router)

######################### PROFISSIONAIS #########################
app.include_router(profissionais.router) # type: ignore

######################### SERVIÇOS #########################
app.include_router(servicos.router) # type: ignore

######################### CLIENTES #########################
app.include_router(clientes.router) # type: ignore

######################### AGENDAMENTOS #########################
app.include_router(agendamentos.router)

########################## AUTENTICAÇÃO #########################
app.include_router(auth.router, tags=["auth"]) # NOVO: Roteador de autenticação