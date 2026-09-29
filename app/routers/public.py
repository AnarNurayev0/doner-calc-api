from fastapi import APIRouter, status, HTTPException
from ..services import currency, calculator
from ..database import DatabaseDep
from app import models


router = APIRouter(prefix="/doner",tags=["Public Endpoints"])

# === PUBLIC ENDPOINTS ===

# --- DONER COUNT ---
@router.get("",status_code=status.HTTP_200_OK)
def doner_count(doner_name: str, meat_type: str, from_currency: str, amount: float, db: DatabaseDep) -> dict:

    doner = db.query(models.Doners).filter(models.Doners.doner_name == doner_name, models.Doners.meat_type == meat_type).first()

    if not doner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Doner is not found!")
    
    try:
        doner_price = doner.model_dump()["price"]
    except:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)

    money = currency.currency_conventer(from_currency, amount)
    data = calculator.count_calculator(doner_price, money)

    doner, change = data

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Doner is not found!") 

    change_money = round(currency.currency_conventer("AZN", change, from_currency), 2)

    return {"doners": doner, f"change({from_currency})": change_money}

