from fastapi import APIRouter, status, HTTPException
from ..services import currency, calculator
from ..database import DatabaseDep
from ..exceptions import TheError
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

    doner_amount, change = data

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Doner is not found!") 

    change_money = round(currency.currency_conventer("AZN", change, from_currency), 1)

    return {"doners": doner_amount, f"change({from_currency})": change_money}

# --- DONER OPTIONS ---
@router.get("/options", status_code=status.HTTP_200_OK)
def doner_options(db: DatabaseDep) -> dict[str, list[dict]]:
    rows = db.query(models.Doners.doner_name, models.Doners.meat_type, models.Doners.price).all()

    result: dict[str, list[dict]] = {}
    for name, meat, price in rows:
        result.setdefault(name, []).append({"meat_type": meat, "price": price})

    return result

# --- CURRENCIES ---
@router.get("/currencies", status_code=status.HTTP_200_OK)
def doner_currencies() -> list[dict]:
    try:
        return currency.get_currencies()
    except TheError:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Currency API unavailable")