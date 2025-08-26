# backend/app/routes/profissionais.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session # type: ignore
from typing import List

from app.database import get_db
from app.models.profissional import Profissional as ProfissionalModel
from app.schemas.profissional import ProfissionalCreate, ProfissionalRead, ProfissionalUpdate
from app.core.security import get_password_hash
from app.dependencies import get_current_salao

router = APIRouter(
    prefix="/profissionais",
    tags=["profissionais"],
)

@router.post(
    "/",
    response_model=ProfissionalRead,
    status_code=status.HTTP_201_CREATED,
)
def create_profissional(
    profissional: ProfissionalCreate,
    db: Session = Depends(get_db),
    current_salao: dict = Depends(get_current_salao),
):
    """
    Cria um novo profissional para um salão.
    """
    # Verifica se o email já existe
    db_profissional = db.query(ProfissionalModel).filter(ProfissionalModel.email == profissional.email).first()
    if db_profissional:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado."
        )

    # Hash da senha antes de salvar
    hashed_password = get_password_hash(profissional.senha)
    
    # Cria a instância do modelo
    db_profissional = ProfissionalModel(
        nome=profissional.nome,
        email=profissional.email,
        senha_hash=hashed_password,
        telefone=profissional.telefone,
        especialidade=profissional.especialidade,
        salao_id=current_salao.id, # Associa o profissional ao salão logado
    )
    
    db.add(db_profissional)
    db.commit()
    db.refresh(db_profissional)
    return db_profissional

@router.get("/", response_model=List[ProfissionalRead])
def read_profissionais(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_salao: dict = Depends(get_current_salao),
):
    """
    Lista todos os profissionais de um salão.
    """
    profissionais = db.query(ProfissionalModel).filter(ProfissionalModel.salao_id == current_salao.id).offset(skip).limit(limit).all()
    return profissionais

@router.get("/{profissional_id}", response_model=ProfissionalRead)
def read_profissional(
    profissional_id: int,
    db: Session = Depends(get_db),
    current_salao: dict = Depends(get_current_salao),
):
    """
    Obtém um profissional por ID, verificando se pertence ao salão logado.
    """
    db_profissional = db.query(ProfissionalModel).filter(
        ProfissionalModel.id == profissional_id,
        ProfissionalModel.salao_id == current_salao.id
    ).first()
    if db_profissional is None:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")
    return db_profissional

@router.put("/{profissional_id}", response_model=ProfissionalRead)
def update_profissional(
    profissional_id: int,
    profissional: ProfissionalUpdate,
    db: Session = Depends(get_db),
    current_salao: dict = Depends(get_current_salao),
):
    """
    Atualiza um profissional por ID, verificando se pertence ao salão logado.
    """
    db_profissional = db.query(ProfissionalModel).filter(
        ProfissionalModel.id == profissional_id,
        ProfissionalModel.salao_id == current_salao.id
    ).first()
    if db_profissional is None:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")

    for key, value in profissional.model_dump(exclude_unset=True).items():
        if key == "senha":
            setattr(db_profissional, "senha_hash", get_password_hash(value))
        else:
            setattr(db_profissional, key, value)
    
    db.commit()
    db.refresh(db_profissional)
    return db_profissional

@router.delete("/{profissional_id}", response_model=dict)
def delete_profissional(
    profissional_id: int,
    db: Session = Depends(get_db),
    current_salao: dict = Depends(get_current_salao),
):
    """
    Deleta um profissional por ID, verificando se pertence ao salão logado.
    """
    db_profissional = db.query(ProfissionalModel).filter(
        ProfissionalModel.id == profissional_id,
        ProfissionalModel.salao_id == current_salao.id
    ).first()
    if db_profissional is None:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")

    db.delete(db_profissional)
    db.commit()
    return {"message": "Profissional deletado com sucesso"}