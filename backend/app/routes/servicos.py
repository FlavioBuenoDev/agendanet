from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session  # type: ignore

from app import schemas, crud
from app.database import get_db

router = APIRouter()

# Endpoint para criar um serviço
@app.post("/servicos/", response_model=schemas.Servico, status_code=status.HTTP_201_CREATED) # type: ignore
def create_servico(servico: schemas.ServicoCreate, db: Session = Depends(get_db)):
    return crud.create_servico(db=db, servico=servico)

# Endpoint para listar serviços
@app.get("/servicos/", response_model=List[schemas.Servico]) # type: ignore
def read_servicos(skip: int = 0, limit: int = 100, db
: Session = Depends(get_db)):
    servicos = crud.get_servicos(db, skip=skip, limit=limit)
    return servicos

# Endpoint para obter um serviço por ID
@app.get("/servicos/{servico_id}", response_model=schemas.Servico) # type: ignore
def read_servico(servico_id: int, db: Session = Depends(get_db)):
    db_servico = crud.get_servico(db, servico_id=servico_id)
    if db_servico is None:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return db_servico

# Endpoint para atualizar um serviço
@app.put("/servicos/{servico_id}", response_model=schemas.Servico) # type: ignore
def update_servico(servico_id: int, servico: schemas.ServicoUpdate, db
: Session = Depends(get_db)):
    db_servico = crud.get_servico(db, servico_id=servico_id)
    if db_servico is None:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return crud.update_servico(db=db, servico_id=servico_id, servico=servico)

# Endpoint para deletar um serviço
@app.delete("/servicos/{servico_id}", status_code=status.HTTP_204_NO_CONTENT)   # type: ignore
def delete_servico(servico_id: int, db: Session = Depends(get_db)):
    db_servico = crud.get_servico(db, servico_id=servico_id)
    if db_servico is None:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    crud.delete_servico(db=db, servico_id=servico_id)
    return {"detail": "Serviço deletado com sucesso"}
