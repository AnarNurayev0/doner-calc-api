from fastapi import APIRouter, status, HTTPException, Depends
from ..database import DatabaseDep
from ..auth import verify_admin
from app import models, schemas


router = APIRouter(prefix="/admin", tags=["Admin Endpoints"], dependencies=[Depends(verify_admin)])

# === ADMIN ENDPOINTS ===

# --- CREATE DONER ---
@router.post("/create",response_model=schemas.DonerOut)
def create_doner(db: DatabaseDep, data: schemas.DonerCreate):

    doner = models.Doners(**data.model_dump())
    db.add(doner)
    db.commit()
    db.refresh(doner)

    return doner