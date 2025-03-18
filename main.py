from fastapi import FastAPI
from database import create_db_tables
from controllers import avist_archivo, archivos, avist, departamento, discord, distrito, noticias, provincia, users, auth

app = FastAPI()

@app.on_event("startup")
def startup():
    create_db_tables()

app.include_router(users.router)
app.include_router(avist.router)
app.include_router(archivos.router)
app.include_router(noticias.router)
app.include_router(departamento.router)
app.include_router(provincia.router)
app.include_router(distrito.router)
app.include_router(avist_archivo.router)
app.include_router(auth.router)
app.include_router(discord.router)