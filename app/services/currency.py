from datetime import datetime, timezone
from ..exceptions import TheError
import requests

BASE_URL = "https://api.fxratesapi.com/convert"
CURRENCIES_URL = "https://api.fxratesapi.com/currencies"


def currency_conventer(from_currency: str, amount: float, to_currency: str = "AZN"):

    today_utc = datetime.now(timezone.utc).date().isoformat()

    params = {
        "from": from_currency,
        "to": to_currency,
        "date": today_utc,
        "amount": amount,
        "format": "json",
    }

    try:
        response = requests.get(BASE_URL, params=params).json()["result"]
    except Exception as e:
        raise TheError(f"Error {e} was occured!") from e

    return response


def get_currencies() -> list[dict]:
    try:
        response = requests.get(CURRENCIES_URL, timeout=10)
        response.raise_for_status()
        raw = response.json()
    except Exception as e:
        raise TheError(f"Error {e} was occured!") from e

    return sorted(
        ({"code": code, "name": info.get("name", code)} for code, info in raw.items()),
        key=lambda c: c["code"],
    )