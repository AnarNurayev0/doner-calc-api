from fastapi import APIRouter, status, HTTPException, Depends
from ..database import DatabaseDep
from ..auth import verify_admin
from app import models, schemas
from typing import List

router = APIRouter(prefix="/admin", tags=["Admin Endpoints"], dependencies=[Depends(verify_admin)])

# === ADMIN ENDPOINTS ===

# -- ALL DONERS ---
@router.get("/all", response_model=List[schemas.DonerOut], status_code=status.HTTP_200_OK)
def create_doner(db: DatabaseDep):

    doners = db.query(models.Doners).all()

    return doners

# --- CREATE DONER ---
@router.post("/create", response_model=schemas.DonerOut, status_code=status.HTTP_201_CREATED)
def create_doner(db: DatabaseDep, data: schemas.DonerCreate):

    doner = models.Doners(**data.model_dump())
    db.add(doner)
    db.commit()
    db.refresh(doner)

    return doner

# --- DELETE DONER ---
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_doner(db: DatabaseDep, id: int):

    doner = db.query(models.Doners).filter(models.Doners.id == id).first()

    if not doner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Doner is not found!")

    db.delete(doner)
    db.commit()

    return

# --- UPDATE DONER ---
@router.put("/update/{id}",status_code=status.HTTP_200_OK,response_model=schemas.DonerOut)
def put_article(doner: schemas.DonerCreate, id: int, db: DatabaseDep):

    db_doner = db.query(models.Doners).filter(id == models.Doners.id).first()

    if not id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    doner_data = doner.model_dump(exclude_unset=True)

    db_doner.sqlmodel_update(doner_data)
    db.add(db_doner)
    db.commit()
    db.refresh(db_doner)

    return db_doner