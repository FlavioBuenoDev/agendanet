# app/routes/clientes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session # type: ignore
from sqlalchemy.exc import IntegrityError # type: ignore
from .. import crud, schemas
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Cliente)
def create_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = crud.get_cliente_by_email(db, email=cliente.email)
    if db_cliente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já cadastrado."
        )
    # envolva a criação em um try...except
    try:
        # Se a verificação acima for removida no futuro,
        # o banco de dados ainda garante a integridade
        return crud.create_cliente(db=db, cliente=cliente)
    except IntegrityError:
        # Se o banco de dados levantar a exceção,
        # nós a capturamos e retornamos um erro HTTP
        db.rollback()  # É importante fazer o rollback da transação
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro de integridade: e-mail ou outro campo único duplicado."
        )