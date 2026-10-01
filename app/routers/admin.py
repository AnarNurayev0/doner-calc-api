from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from ..database import DatabaseDep
from ..redis import redis_client
from app import models, schemas
from ..auth import verify_admin
from typing import List
import json

router = APIRouter(
    prefix="/admin",
    tags=["Admin Endpoints"],
    dependencies=[Depends(verify_admin)],
)

# === ADMIN ENDPOINTS ===


# --- ALL DONERS ---
@router.get(
    "/all", response_model=List[schemas.DonerOut], status_code=status.HTTP_200_OK
)
def all_doners(db: DatabaseDep):

    cache_key = "all_doners:admin"
    cached_response = redis_client.get(cache_key)

    if cached_response:
        return json.loads(cached_response)

    doners = db.query(models.Doners).all()

    doners_json = jsonable_encoder(doners)
    redis_client.set(cache_key, json.dumps(doners_json), ex=300)

    return doners


# --- CREATE DONER ---
@router.post(
    "/create",
    response_model=schemas.DonerOut,
    status_code=status.HTTP_201_CREATED,
)
def create_doner(db: DatabaseDep, data: schemas.DonerCreate):

    doner = models.Doners(**data.model_dump())
    db.add(doner)
    db.commit()
    db.refresh(doner)

    redis_client.delete("all_doners:admin")
    redis_client.delete("doner_options:public")

    return doner


# --- DELETE DONER ---
@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doner(db: DatabaseDep, id: int):

    doner = db.query(models.Doners).filter(models.Doners.id == id).first()

    if not doner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Doner is not found!"
        )

    db.delete(doner)
    db.commit()

    redis_client.delete("all_doners:admin")
    redis_client.delete("doner_options:public")

    return


# --- UPDATE DONER ---
@router.put(
    "/update/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.DonerOut,
)
def update_doner(doner: schemas.DonerCreate, id: int, db: DatabaseDep):

    db_doner = db.query(models.Doners).filter(models.Doners.id == id).first()

    if not db_doner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Doner with id:{id} not found!",
        )

    doner_data = doner.model_dump(exclude_unset=True)

    db_doner.sqlmodel_update(doner_data)
    db.add(db_doner)
    db.commit()
    db.refresh(db_doner)

    redis_client.delete("all_doners:admin")
    redis_client.delete("doner_options:public")

    return db_doner