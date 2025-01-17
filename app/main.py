from fastapi import FastAPI, Depends
from .web import inventory, member
from app.models.database import get_db

app = FastAPI(dependencies=[Depends(get_db)])
app.include_router(inventory.router)
app.include_router(member.router)


@app.get("/")
async def root():
    return "Hello World!"
