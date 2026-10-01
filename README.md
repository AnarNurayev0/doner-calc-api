# Doner-Calc

A small FastAPI project that answers one question: **how many doners can you buy with the money you have in Azerbaijan?**

Pick a doner and a meat type, enter an amount in any currency, and the API converts it to AZN, calculates how many doners you can buy and returns the change in your original currency. A simple web page is served by the same app, so there is no separate frontend to deploy.

**Live demo:** https://doner-calc-api.onrender.com/

> The demo runs on Render's free tier, so the first request after a period of inactivity can take up to a minute while the service wakes up.

## Features

- Works with the currencies supported by [fxratesapi](https://fxratesapi.com) (the list is fetched live)
- Returns the number of doners and the change in the currency you paid with
- Doner names, meat types and prices live in PostgreSQL, so prices can be changed without touching the code
- Admin endpoints (HTTP Basic auth) to list, create, update and delete doners
- Redis caching for calculations, options, currencies and admin lists
- Built-in web page at `/`, styled as a receipt
- Database migrations with Alembic
- Health check endpoint for uptime monitoring

## Tech stack

- Python, FastAPI
- SQLModel, SQLAlchemy, PostgreSQL (`psycopg`)
- Alembic
- Redis
- fxratesapi for exchange rates
- Plain HTML, CSS and JS for the frontend

## Project structure

```
Doner-Calc/
├── alembic/
│   └── versions/
├── app/
│   ├── routers/
│   │   ├── public.py
│   │   └── admin.py
│   ├── services/
│   │   ├── calculator.py
│   │   └── currency.py
│   ├── static/
│   │   ├── index.html
│   │   ├── favicon.svg
│   │   └── apple-touch-icon.png
│   ├── auth.py
│   ├── database.py
│   ├── exceptions.py
│   ├── main.py
│   ├── models.py
│   ├── redis.py
│   ├── schemas.py
│   └── settings.py
├── alembic.ini
├── LICENSE
├── README.md
└── requirements.txt
```

## Getting started

You need Python, a running PostgreSQL database and a running Redis instance.

```bash
git clone https://github.com/AnarNurayev0/doner-calc-api.git
cd doner-calc-api
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the project root with these variables:

```
CURRENCY_API_TOKEN=
DATABASE_HOSTNAME=
DATABASE_PORT=
DATABASE_NAME=
DATABASE_USERNAME=
DATABASE_PASSWORD=
ADMIN_USERNAME=
ADMIN_PASSWORD=
REDIS_URL=
```

| Variable | Description |
|---|---|
| `CURRENCY_API_TOKEN` | API token for fxratesapi |
| `DATABASE_*` | PostgreSQL connection details |
| `ADMIN_USERNAME`, `ADMIN_PASSWORD` | Credentials for the `/admin` endpoints |
| `REDIS_URL` | Redis connection string, e.g. `redis://localhost:6379/0` |

All variables are required, the app will not start without them.

Apply the migrations and start the server:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/` for the web page or `http://127.0.0.1:8000/docs` for the interactive API docs.

The database starts empty. Add doners with the admin endpoints before using the calculator.

## API

### Calculate

```
GET /doner?doner_name=Hatay usulu&meat_type=Toyuq&from_currency=USD&amount=100
```

| Parameter | Type | Description |
|---|---|---|
| `doner_name` | string | Name of the doner |
| `meat_type` | string | Meat type of that doner |
| `from_currency` | string | Currency code of the money you have (USD, EUR, TRY, ...) |
| `amount` | float | How much money you have |

Response:

```json
{
  "doners": 12,
  "change(USD)": 3.5
}
```

The change key includes the currency you sent. Prices are stored in AZN, and the change is converted back to your currency (rounded to one decimal place).

If the doner and meat type combination does not exist, the API returns `404` with `Doner is not found!`.

Results are cached in Redis for 2 minutes.

### Options

```
GET /doner/options
```

Returns every doner with its available meat types and prices (in AZN). The web page uses this to fill the dropdowns and show the price next to each choice.

```json
{
  "Hatay usulu": [
    {"meat_type": "Ət", "price": 5},
    {"meat_type": "Toyuq", "price": 4}
  ]
}
```

### Currencies

```
GET /doner/currencies
```

Returns the list of supported currencies, sorted by code. The list is cached for 1 hour. If the exchange rate provider is down, the API returns `502`.

```json
[
  {"code": "AED", "name": "United Arab Emirates Dirham"},
  {"code": "AZN", "name": "Azerbaijani Manat"}
]
```

### Health

```
GET /health
```

Returns `200` when the app is running.

### Admin

All admin endpoints are under `/admin` and require HTTP Basic authentication with `ADMIN_USERNAME` and `ADMIN_PASSWORD`.

| Method | Path | Description |
|---|---|---|
| GET | `/admin/all` | List all doners |
| POST | `/admin/create` | Add a new doner |
| PUT | `/admin/update/{id}` | Update a doner |
| DELETE | `/admin/delete/{id}` | Delete a doner |

Request body for create and update (prices are in AZN):

```json
{
  "doner_name": "Hatay usulu",
  "meat_type": "Toyuq",
  "price": 4
}
```

Example:

```bash
curl -u admin:password -X POST http://127.0.0.1:8000/admin/create \
  -H "Content-Type: application/json" \
  -d '{"doner_name": "Hatay usulu", "meat_type": "Toyuq", "price": 4}'
```

Create, update and delete clear the related cache entries, so changes show up immediately.

## Deployment

The app runs as a single Web Service on [Render](https://render.com), together with a Render PostgreSQL database and a Redis (Key Value) instance.

| Setting | Value |
|---|---|
| Build command | `pip install -r requirements.txt` |
| Start command | `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

Add every variable from the `.env` list above to the service environment. The database is empty after the first deploy, so add the doners through the admin endpoints.

## License

Released under the MIT License. See [LICENSE](LICENSE).