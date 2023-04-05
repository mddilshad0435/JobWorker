from WebCore.api.base import app, templates
from WebCore.api.job import job_router, Request
from WebCore.api.role import role_router
from WebCore.api.status import status_router
from WebCore.api.user import user_router
from WebCore.db.engine import init_engine
from WebCore.api.googleAuth import authRouter
import WebCore.static_DB.static_db as static_db

from WebCore.models.base import Base
from WebCore.api.static_route import static_router
from sqlalchemy.sql import text
import os
from starlette.middleware.sessions import SessionMiddleware

app.include_router(job_router)
app.include_router(role_router)
app.include_router(status_router)
app.include_router(user_router)
app.include_router(static_router)
app.include_router(authRouter)

# Set up the middleware to read the request session
SECRET_KEY = "P0JC+wnMn7dp2gMZRQI7SQasxBrjeAGgIr50RE6u"
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

@app.get("/home/", tags=["home"])
def home(request: Request):    
    return templates.TemplateResponse("account-signup.html", {"request": request})

@app.get("/")
async def Index(request: Request):
    static_db.creating_db()
    data = init_engine.execute(text("SELECT to_regclass('public.countries');"))
    for i in data:
        countries = i
    if not countries[0]:
        with open("WebCore/CountryStatesCities/countries.sql", 'r') as f:
            countryQuery = f.read()
        init_engine.execute(countryQuery)
        print("Updated countries data in tables")

    data = init_engine.execute(text("SELECT to_regclass('public.states');"))
    for i in data:
        states = i
    if not states[0]:
        with open("WebCore/CountryStatesCities/states.sql", 'r') as f:
            statesQuery = f.read()
        init_engine.execute(statesQuery)
        print("Updated states data in tables")
    
    data = init_engine.execute(text("SELECT to_regclass('public.cities');"))
    for i in data:
        cities = i
    if not cities[0]:
        with open("WebCore/CountryStatesCities/cities.sql", 'r') as f:
            citiesQuery = f.read()
        init_engine.execute(citiesQuery)
        print("Updated cities data in tables")

    return templates.TemplateResponse("index.html",{"request":request})


Base.metadata.create_all(bind=init_engine)
