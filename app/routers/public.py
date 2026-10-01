from fastapi import APIRouter, status, HTTPException
from ..services import currency, calculator
from ..database import DatabaseDep
from ..exceptions import TheError
from ..redis import redis_client
from app import models
import json

router = APIRouter(prefix="/doner",tags=["Public Endpoints"])

# === PUBLIC ENDPOINTS ===

# --- DONER COUNT ---
@router.get("",status_code=status.HTTP_200_OK)
def doner_count(doner_name: str, meat_type: str, from_currency: str, amount: float, db: DatabaseDep) -> dict:

    cache_key = f"doner_count:{doner_name}:{meat_type}:{from_currency}:{amount}"
    cached_product = redis_client.get(cache_key)

    if cached_product:
        return json.loads(cached_product)

    doner = db.query(models.Doners).filter(models.Doners.doner_name == doner_name, models.Doners.meat_type == meat_type).first()

    if not doner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Doner is not found!")
    
    # try:
    #     doner_price = doner.model_dump()["price"]
    # except:
    #     raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)

    doner_price = doner.price

    money = currency.currency_conventer(from_currency, amount)
    data = calculator.count_calculator(doner_price, money)

    doner_amount, change = data

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Doner is not found!") 

    change_money = round(currency.currency_conventer("AZN", change, from_currency), 1)

    response = {"doners": doner_amount, f"change({from_currency})": change_money}
    
    redis_client.set(cache_key, json.dumps(response), ex=120)

    return response

# --- DONER OPTIONS ---
@router.get("/options", status_code=status.HTTP_200_OK)
def doner_options(db: DatabaseDep) -> dict[str, list[dict]]:

    cache_key = f"doner_options:public"
    cached_product = redis_client.get(cache_key)
    
    if cached_product:
        return json.loads(cached_product)
    
    rows = db.query(models.Doners.doner_name, models.Doners.meat_type, models.Doners.price).all()

    result: dict[str, list[dict]] = {}
    for name, meat, price in rows:
        result.setdefault(name, []).append({"meat_type": meat, "price": price})

    redis_client.set(cache_key, json.dumps(result), ex=120)

    return result

# --- CURRENCIES ---
@router.get("/currencies", status_code=status.HTTP_200_OK)
def doner_currencies() -> list[dict]:

    cache_key = f"doner_currencies:public"
    cached_product = redis_client.get(cache_key)
    
    if cached_product:
        return json.loads(cached_product)

    try:
        currency_data = currency.get_currencies()
        redis_client.set(cache_key, json.dumps(currency_data), ex=3600)
        return currency_data
    
    except TheError:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Currency API unavailable")