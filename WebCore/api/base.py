import os
from dotenv import load_dotenv
from pathlib import Path

from fastapi import FastAPI
from WebCore.models.status import Status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi_sqlalchemy import DBSessionMiddleware, db
from WebCore.db.engine import SQLALCHEMY_DATABASE_URL

load_dotenv('.env')

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory="templates")
print(BASE_DIR)

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=SQLALCHEMY_DATABASE_URL)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Base.metadata.create_all(bind=init_engine)

def get_status_obj(name, category):
    status_obj = db.session.query(Status).filter(Status.name==name,Status.category==category).first()
    return status_obj