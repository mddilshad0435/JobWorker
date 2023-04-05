from fastapi import APIRouter, Request, templating, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from WebCore.auth.jwt_handler import decodeJWT
from WebCore.auth.oauth2 import get_current_user
from WebCore.schemas.request.user import UserModel,UserDetails,userAddressSchema
from fastapi_sqlalchemy import db
from WebCore.models.user import User, Address
from fastapi.encoders import jsonable_encoder
from WebCore.db.engine import init_engine
from sqlalchemy.sql import text

templates = Jinja2Templates(directory="templates")

static_router = APIRouter()

def query_to_dict(query_list):
    data = []
    for post in query_list:
        json_compatible_item_data = jsonable_encoder(post)
        data.append(json_compatible_item_data)
    return data

def user_email_name(currentuser):
    userdata = db.session.query(User).filter(User.email==currentuser.email).first().first_name
    details={"email":currentuser.email,"fullname":userdata}
    return details

@static_router.get("/intro/")
async def get_intro(request: Request):
    return templates.TemplateResponse("intro.html",{"request":request})



@static_router.get("/user/details/")
async def accountsDetails(request: Request):
    return templates.TemplateResponse("account-details.html",{"request":request})

@static_router.post("/user/details/")
async def accountDetailsPost(request: Request, currentuser: UserModel = Depends(get_current_user)):
    if not currentuser:
        return JSONResponse({"msg":"Please Login"},status_code=400)
    # details = user_email_name(currentuser)
    # print(details)
    userdata = db.session.query(User).filter(User.email==currentuser.email)
    userdata = query_to_dict(userdata)
    # print(userdata)
    countries = init_engine.execute(text("SELECT id, name FROM countries order by name;"))
    countries = query_to_dict(countries)

    userId = db.session.query(User).filter(User.email==currentuser.email).first()
    address = db.session.query(Address).filter(Address.user_id==userId.id)
    if address.first():
        address = query_to_dict(address)
        
        states = init_engine.execute(text(f"SELECT id, name FROM states where country_id={address[0]['country_id']} order by name;"))
        states = query_to_dict(states)
        cities = init_engine.execute(text(f"SELECT id, name from cities where state_id={address[0]['state_id']} order by name;"))
        cities = query_to_dict(cities)
        # print("++++++++++++",address,states)
        return JSONResponse({"msg":"Done","details":userdata[0],"countries":countries,
                "address":address[0],"states":states, "cities":cities})
    return JSONResponse({"msg":"Done","details":userdata[0],"countries":countries, "address":[]})


@static_router.post("/states/")
async def AllStates(request: Request):
    countryId = await request.json()
    print(countryId)
    states = init_engine.execute(text(f"SELECT id, name FROM states where country_id={countryId} order by name;"))
    states = query_to_dict(states)
    print(states)
    return JSONResponse({"states":states})

@static_router.post("/cities")
async def AllCities(request: Request):
    data = await request.json()
    print(data,data['stateId'])
    cities = init_engine.execute(text(f"SELECT id, name from cities where state_id={data['stateId']} order by name;"))
    cities = query_to_dict(cities)
    return JSONResponse({"cities":cities})

@static_router.get("/user/security/")
async def accountSecurity(request: Request):
    return templates.TemplateResponse("account-security.html", {"request": request})


@static_router.post("/user/security/")
async def accountSecurityPost(request: Request, currentuser: UserModel = Depends(get_current_user)): 
    if not currentuser:
        return JSONResponse({"msg":"Please Login"},status_code=400)
    details = user_email_name(currentuser)
    return JSONResponse({"msg":"Done","details":details})


@static_router.get("/user/collections/")
async def accountsCollections(request: Request):
    return templates.TemplateResponse("account-collections.html",{"request":request})

@static_router.post("/user/collections/")
async def accountCollectionsPost(request: Request,  currentuser: UserModel = Depends(get_current_user)):
    if not currentuser:
        return JSONResponse({"msg":"Please Login"},status_code=400)
    details = user_email_name(currentuser)
    return JSONResponse({"msg":"Done","details":details})

@static_router.get("/about/")
async def about_view(request: Request):
    return templates.TemplateResponse("about.html",{"request":request})


@static_router.post("/user/address/")
async def address_save(useraddress: userAddressSchema, currentuser: UserModel = Depends(get_current_user)):
    if not currentuser:
        return JSONResponse({"msg":"Please Login"},status_code=400)
    userId = db.session.query(User).filter(
            User.email == currentuser.email).first()
    if not userId:
        return JSONResponse(status_code=400, content={"msg": "invalid"})
    print(useraddress,userId.id)
    address = db.session.query(Address).filter(Address.user_id==userId.id).first()
    if not address:
        addr = Address(
            country_id = useraddress.country_id,
            state_id = useraddress.state_id,
            city_id = useraddress.city_id,
            zipCode = useraddress.zip,
            address1 = useraddress.address,
            address2 = useraddress.address2,
            user_id = userId.id
        )
        db.session.add(addr)
        db.session.commit()
        return JSONResponse({"msg":"Address Added"})

    address.country_id = useraddress.country_id
    address.state_id = useraddress.state_id
    address.city_id = useraddress.city_id
    address.zipCode = useraddress.zip
    address.address1 = useraddress.address
    address.address2 = useraddress.address2
    db.session.add(address)
    db.session.commit()

    return JSONResponse({"msg":"Address Updated"})
    