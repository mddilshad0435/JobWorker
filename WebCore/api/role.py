from fastapi import APIRouter
from dotenv import load_dotenv

from fastapi.responses import JSONResponse
from fastapi_sqlalchemy import db

from WebCore.schemas.request.role import RoleSchema

from WebCore.models.role import Role

load_dotenv('.env')

role_router = APIRouter()


@role_router.post('/role/')
def creating_role(role: RoleSchema):

    db_role = Role(
        name=role.name,
    )
    db.session.add(db_role)
    db.session.commit()

    return JSONResponse(status_code=200)


@role_router.get('/role/')
def get_role():

    return db.session.query(Role).all()
