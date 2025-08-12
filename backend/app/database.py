import os
from dotenv import load_dotenv
from sqlalchemy import create_engine # type: ignore
#from sqlalchemy.ext.declarative import declarative_base # type: ignore
#from sqlalchemy.orm import declarative_base # type: ignore # Apenas mude o 'ext.declarative' para 'orm' (Atualização de acordo com a documentação mais recente do SQLAlchemy)
from sqlalchemy.orm import sessionmaker, declarative_base # type: ignore

from app.models import Base # <-- Agora a Base vem de models

from app import models

load_dotenv() # Carrega as variáveis do .env - **Esta linha deve vir antes de usar os.getenv()**

# Configuração do MySQL - Lendo DO ARQUIVO .env
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "mysql") # <-- Sua senha REAL do MySQL
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DB = os.getenv("MYSQL_DB", "salao_agendamento_db")

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
                       
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        