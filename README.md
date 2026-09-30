# Doner-Calc

A small FastAPI project that answers one question: how many doners can you buy with the money you have?

Pick a doner and a meat type, enter an amount in any currency, and the API converts it to AZN, calculates how many doners you can buy and returns the change in your original currency. A simple web page is served by the same app, so there is no separate frontend to deploy.

## Features

- Works with any currency supported by [fxratesapi](https://fxratesapi.com)
- Returns the number of doners and the change in the currency you paid with
- Doner names, meat types and prices are stored in PostgreSQL, so prices can be changed without touching the code
- Admin endpoints to list, create, update and delete doners
- Built-in web page at `/`, styled as a receipt
- Database migrations with Alembic

## Tech stack

- Python, FastAPI
- SQLModel, PostgreSQL
- Alembic
- fxratesapi for exchange rates
- Plain HTML, CSS and JS for the frontend

## Project structure

```
Doner-Calc/
├── alembic/
├── app/
│   ├── routers/
│   │   ├── public.py
│   │   └── admin.py
│   ├── services/
│   │   ├── calculator.py
│   │   └── currency.py
│   ├── static/
│   │   └── index.html
│   ├── auth.py
│   ├── database.py
│   ├── exceptions.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── settings.py
├── alembic.ini
├── DESIGN.md
├── LICENSE
├── README.md
└── requirements.txt
```

## Getting started

You need Python and a running PostgreSQL database.

```bash
git clone https://github.com/AnarNurayev0/doner-calc-api.git
cd doner-calc-api
python -m venv venv
source venv/bin/activate
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
```

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

The change key includes the currency you sent. Prices are stored in AZN, and the change is converted back to your currency.

If the doner and meat type combination does not exist, the API returns `404` with `Doner is not found!`.

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

### Admin

All admin endpoints are under `/admin` and require the admin credentials.

| Method | Path | Description |
|---|---|---|
| GET | `/admin/all` | List all doners |
| POST | `/admin/create` | Add a new doner |
| PUT | `/admin/update/{id}` | Update a doner |
| DELETE | `/admin/delete?id=` | Delete a doner |

Request body for create and update (prices are in AZN):

```json
{
  "doner_name": "Hatay usulu",
  "meat_type": "Toyuq",
  "price": 4
}
```

## Deployment

The app runs as a single Web Service on [Render](https://render.com) with a Render PostgreSQL database.

| Setting | Value |
|---|---|
| Build command | `pip install -r requirements.txt` |
| Start command | `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

Add every variable from the `.env` list above to the service environment. The database is empty after the first deploy, so add the doners again through the admin endpoints.

## Design

Colors, fonts and layout rules for the web page are in [DESIGN.md](DESIGN.md).

## License

See [LICENSE](LICENSE).
