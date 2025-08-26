# app/routes/clientes.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session # type: ignore
from datetime import timedelta
from typing import Annotated, List

from app import schemas, crud, models
from app.database import get_db
from app.core.security import get_password_hash # Importa a função de hash
from .auth import get_current_active_cliente, get_current_active_salao

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)

@router.post("/", response_model=schemas.ClienteRead, status_code=status.HTTP_201_CREATED)
def create_cliente(
    cliente: schemas.ClienteCreate,
    db: Session = Depends(get_db),
    # Sintaxe de dependência padrão para evitar erros
    current_salao: models.Salao = Depends(get_current_active_salao)
):
    """
    Cria um novo cliente para o salão logado.
    """
    db_cliente = crud.get_cliente_by_email(db, email=cliente.email)
    if db_cliente:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado")

    # Hasheia a senha antes de criar o cliente
    hashed_password = get_password_hash(cliente.senha)
    
    # Cria uma nova instância do schema com a senha hasheada
    cliente_com_hash = schemas.ClienteCreate(
        nome=cliente.nome,
        email=cliente.email,
        telefone=cliente.telefone,
        senha=hashed_password,
        salao_id=current_salao.id
    )
    
    return crud.create_cliente(db=db, cliente=cliente_com_hash, salao_id=current_salao.id)

@router.get("/me/", response_model=schemas.ClienteRead)
async def read_clientes_me(current_cliente: Annotated[models.Cliente, Depends(get_current_active_cliente)]):
    """
    Obtém as informações do cliente logado.
    """
    return current_cliente

@router.get("/", response_model=List[schemas.ClienteRead])
def read_clientes(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    # Sintaxe de dependência padrão para evitar erros
    current_salao: models.Salao = Depends(get_current_active_salao)
):
    """
    Lista todos os clientes associados ao salão logado.
    """
    clientes = crud.get_clientes_by_salao(db, salao_id=current_salao.id, skip=skip, limit=limit)
    return clientes

@router.get("/{cliente_id}", response_model=schemas.ClienteRead)
def read_cliente(
    cliente_id: int, 
    db: Session = Depends(get_db),
    # Sintaxe de dependência padrão para evitar erros
    current_salao: models.Salao = Depends(get_current_active_salao)
):
    """
    Obtém um cliente específico pelo ID.
    """
    db_cliente = crud.get_cliente(db, cliente_id=cliente_id)
    if db_cliente is None or db_cliente.salao_id != current_salao.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado")
    return db_cliente

@router.put("/{cliente_id}", response_model=schemas.ClienteRead)
def update_cliente(
    cliente_id: int, 
    cliente: schemas.ClienteUpdate,
    db: Session = Depends(get_db),
    # Sintaxe de dependência padrão para evitar erros
    current_cliente: models.Cliente = Depends(get_current_active_cliente)
):
    """
    Atualiza um cliente.
    """
    if cliente_id != current_cliente.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a atualizar este cliente")
    
    db_cliente = crud.update_cliente(db=db, cliente_id=cliente_id, cliente=cliente)
    if db_cliente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado")
    return db_cliente

@router.delete("/{cliente_id}")
def delete_cliente(
    cliente_id: int, 
    db: Session = Depends(get_db),
    # Sintaxe de dependência padrão para evitar erros
    current_cliente: models.Cliente = Depends(get_current_active_cliente)
):
    """
    Deleta um cliente.
    """
    if cliente_id != current_cliente.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a deletar este cliente")
        
    db_cliente = crud.delete_cliente(db=db, cliente_id=cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado")
    return {"message": "Cliente deletado com sucesso", "id": cliente_id}
