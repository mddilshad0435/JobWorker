from fastapi.responses import JSONResponse
from fastapi_sqlalchemy import db
from fastapi import APIRouter

from WebCore.schemas.request.status import StatusSchema

from WebCore.models.status import Status


status_router = APIRouter()


@status_router.post('/status/')
def creating_status(status: StatusSchema):

    db_status = Status(
        name=status.name,
        category=status.category
    )
    db.session.add(db_status)
    db.session.commit()

    return JSONResponse(status_code=200)


@status_router.get('/status/')
def get_status():

    return db.session.query(Status).all()
