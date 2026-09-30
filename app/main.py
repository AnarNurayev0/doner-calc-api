from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, status
from .routers import public, admin
from pathlib import Path

tags_metadata = [
    {
        "name": "Public Endpoints",
        "description": "Public endpoints to calculate how many doners a given budget can buy.."
    },
    {
        "name": "Admin Endpoints",
        "description": "Admin Endpoints"
    },
    {
        "name": "Root",
        "description": "Root"
    },
]

app = FastAPI(openapi_tags=tags_metadata)

app.include_router(public.router)
app.include_router(admin.router)


STATIC_DIR = Path(__file__).parent / "static"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", include_in_schema=False)
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health",status_code=status.HTTP_200_OK,tags=["Health"])
async def health():
    
    return {"heatlh": "OK!"}