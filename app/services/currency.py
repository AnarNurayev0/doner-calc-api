from datetime import datetime, timezone
from ..exceptions import TheError
import requests

BASE_URL = f"https://api.fxratesapi.com/convert"


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