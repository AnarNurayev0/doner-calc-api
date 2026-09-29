from fastapi import FastAPI, status
from .routers import public, admin


tags_metadata = [
    {
        "name": "Public Endpoints",
        "description": "Public endpoints to calculate how many doners a given budget can buy.."
    },
    {
        "name": "Root",
        "description": "Root"
    },
    {
        "name": "Admin Endpoints",
        "description": "Admin Endpoints"
    }
]

app = FastAPI(openapi_tags=tags_metadata)

app.include_router(public.router)
app.include_router(admin.router)


@app.get("/",status_code=status.HTTP_200_OK,tags=["Root"])
async def root():
    
    return {"message": "This is the root url!"}