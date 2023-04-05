from fastapi import Request, Response, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi_sqlalchemy import db

from WebCore.auth.jwt_handler import decodeJWT, encodeJWT, validUser

from WebCore.schemas.request.user import UserLoginSchema, UserSignupSchema, UserResetSchema, UserModel, UserDetails

from WebCore.models.user import User
from WebCore.models.job import Job
from WebCore.models.status import Status
from WebCore.models.cost_negotitation import CostNegotiation
from WebCore.models.worker_job import WorkerJob
from WebCore.schemas.response.user import UserResponseWithToken
from WebCore.api.base import templates, get_status_obj
from WebCore.core.hashing import Hasher
from WebCore.auth.oauth2 import get_current_user

from fastapi import APIRouter


user_router = APIRouter()

def validUserEmail(email,name):
    user_id = db.session.query(User).filter(
            User.email == email).first()
    if user_id:
        data  = {
        "msg": "valid",
        "user_type": user_id.role_id
        }
        return data
    else:
        userdata = User(
            first_name=name,
            email=email,
            role_id=3
        )
        db.session.add(userdata)
        db.session.commit()
        return False


@user_router.get("/user/create_worker/", tags=["home"])
def home(request: Request):
    return templates.TemplateResponse("create_worker.html", {"request": request})

@user_router.post("/user_type/")
async def user_type(request: Request,response: Response):
    access_token = request.cookies.get("access_token")
    if not access_token:
        return JSONResponse(status_code=400, content={"msg": "Please login"})
    data = access_token.split()[1]
    currentuser = validUser(data)

    user_id = db.session.query(User).filter(
            User.email == currentuser.email).first()

    try:
        user_type = user_id.role_id
    except:
        user_type = 0

    return JSONResponse({"user_type":user_type})

@user_router.post("/user/logout/")
async def logout(request: Request,response: Response, currentuser: UserModel = Depends(get_current_user)):
    if not currentuser:
        return JSONResponse(status_code=400, content={"msg": "login"})
    user_id = db.session.query(User).filter(
            User.email == currentuser.email).first()
    if not user_id:
        return JSONResponse(status_code=400, content={"msg": "login"})
    
    response = JSONResponse({"msg":"logout"})
    response.delete_cookie("access_token")
    return response

@user_router.post("/user/alldetails/")
def user_alldetails(user: UserDetails, response: Response,currentuser: UserModel = Depends(get_current_user)):
    if not currentuser:
        return JSONResponse(status_code=400, content={"msg": "Please Login again!"})
    if user.email != currentuser.email:
        user_obj = db.session.query(User).filter(User.email == user.email)
        if user_obj.first():
            return JSONResponse(status_code=400, content={"msg": "Email Already Register!"})

    user_obj = db.session.query(User).filter(User.email == currentuser.email).first()
    if not user_obj:
        return JSONResponse(status_code=400, content={"msg": "Cant update! Please retry later."})
    try: 
        user_obj.first_name = user.first_name
        user_obj.last_name = user.last_name
        user_obj.email = user.email
        user_obj.mobile = user.mobile
        user_obj.bio = user.bio
        db.session.add(user_obj)
        db.session.commit()

        access_token = encodeJWT(user.email)
        response = JSONResponse({'msg':"done"})
        response.delete_cookie("access_token")
        response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
        return response
    except Exception as e:
        return JSONResponse(status_code=400, content={"msg": str(e)})



@user_router.post('/user/signup/')
def creating_user(user: UserSignupSchema, response: Response):
    print(user)
    user_obj = db.session.query(User).filter(User.email == user.email)
    if user_obj.first():
        return JSONResponse(status_code=400, content={"msg": "Already Register!"})
    elif user.password!=user.confirm_password:
        return JSONResponse(status_code=400,content={"msg": "Password not match"})
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=Hasher.get_password_hash(user.password),
        username=user.username,
        role_id=user.role_id
    )

    db.session.add(db_user)
    db.session.commit()
    if user.role_id != 2:
        access_token = encodeJWT(user.email)
        response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)

    user_signup = {
        "msg": "valid",
        "user_type": user.role_id
    }
    user_signup_schema = UserResponseWithToken(**user_signup)
    return user_signup_schema

@user_router.get("/user/login/")
async def login_get(request: Request):
    return templates.TemplateResponse("account-signin.html",{"request":request})

@user_router.post('/user/login/')
def login_user(user: UserLoginSchema, response: Response):
    user_obj = db.session.query(User).filter(
        User.email == user.email)
    user_obj = user_obj.first()

    if not user_obj:
        return JSONResponse(status_code=400, content={"msg": "User is not valid"})

    if not Hasher.verify_password(user.password, user_obj.password):
        return JSONResponse(status_code=400, content={"msg": "User or Password is not valid"})

    access_token = encodeJWT(user_obj.email)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)

    user_signup = {
        "msg": "valid",
        "user_type": user_obj.role_id
    }
    user_signup_schema = UserResponseWithToken(**user_signup)
    return user_signup_schema


@user_router.get('/user/password_reset/')
def reset_password(request: Request):
    return templates.TemplateResponse('password_reset.html', {"request": request})


@user_router.post('/user/password_reset/')
def reset_password(user: UserResetSchema):
    user_obj = db.session.query(User).filter(
        User.email == user.email)
    user_obj = user_obj.first()

    if not user_obj:
        return JSONResponse(status_code=400, content={"msg": "User is not valid"})
    if not Hasher.verify_password(user.old_password, user_obj.password):
        return JSONResponse(status_code=400, content={"msg": "User or Password is not valid"})

    user_obj.password = Hasher.get_password_hash(user.new_password)
    db.session.add(user_obj)
    db.session.commit()

    return JSONResponse(status_code=200)


@user_router.get('/users/')
def get_user():
    return db.session.query(User).all()


@user_router.get('/user/customer/')
def get_data_customer(request: Request):
    return templates.TemplateResponse("customers.html", {"request": request})


def query_to_dict(query_list):
    data = []
    for post in query_list:
        json_compatible_item_data = jsonable_encoder(post)
        data.append(json_compatible_item_data)
    return data

def get_current_status_name(status_id):
    return db.session.query(Status).filter(Status.id == status_id).first().name

def get_price_from_cost_negotiation(post_id):
    try:
        return db.session.query(CostNegotiation).filter(CostNegotiation.job_id == post_id).first().cost
    except:
        return "null"

@user_router.post('/user/customer/')
async def post_data_customer(request: Request, currentuser: UserModel =Depends(get_current_user)):
    if not currentuser:
        return JSONResponse(status_code=400, content={"url": "/user/login/"})
    user_id = db.session.query(User).filter(
            User.email == currentuser.email).first()
    if not user_id:
        return JSONResponse(status_code=400, content={"msg": "invalid"})
    
    total_post = db.session.query(Job).filter(Job.customer_id == user_id.id)

    main_post = query_to_dict(total_post)

    for post in main_post:
        post['current_status'] = get_current_status_name(post['status_id'])
        post['price'] = get_price_from_cost_negotiation(post['id'])

    return JSONResponse({
        'msg': 'valid',
        'main_jobs': main_post
    })


@user_router.get('/user/worker/')
def get_data_worker(request: Request):
    return templates.TemplateResponse("workers.html", {"request": request})


def get_title_desciption(job_id):
    job_obj = db.session.query(Job).filter(Job.id == job_id).first()
    return job_obj.title, job_obj.description


@user_router.post('/user/worker/')
async def post_data_worker(request: Request, currentuser: UserModel =Depends(get_current_user)):
    if not currentuser:
        return JSONResponse(status_code=400, content={"url": "/user/login/"})
    user_id = db.session.query(User).filter(
        User.email == currentuser.email).first()
    if not user_id:
        return JSONResponse(status_code=400, content={"msg": "Invalid"})
        
    all_jobs =list()

    if user_id.role_id == 2:

        jobs = db.session.query(WorkerJob).filter(
            WorkerJob.worker_id == user_id.id)
        all_jobs = query_to_dict(jobs)
        for job in all_jobs:
            job['current_status'] = get_current_status_name(job['status_id'])
            job['title'], job['description'] = get_title_desciption(job['job_id'])
    return JSONResponse({
        'msg': 'valid',
        "all_jobs": all_jobs
    })


def get_worker_from_post_id(post_id):
    worker_obj = db.session.query(WorkerJob).filter(
        WorkerJob.job_id == post_id).first()
    try:
        return db.session.query(User).filter(User.id == worker_obj.worker_id).first().username
    except:
        return "null"

@user_router.get('/user/superuser/')
def get_data_superuser(request: Request):
    return templates.TemplateResponse("superuser.html", {"request": request})


def get_s3_path_from_post_id(post_id):
    try:
        return db.session.query(WorkerJob).filter(WorkerJob.job_id == post_id).first().job_repo_path
    except:
        return "null"

@user_router.post('/user/superuser/')
async def post_data_superuser(request: Request, currentuser: UserModel = Depends(get_current_user)):
    if not currentuser:
        return JSONResponse(status_code=400, content={"url": "/user/login/"})
    user_id = db.session.query(User).filter(
        User.email == currentuser.email).first()
    if not user_id:
        return JSONResponse(status_code=400, content={"msg", "invalid"})
    workers,main_post = list(),list()

    if user_id.role_id == 1:
        total_post = db.session.query(Job).all()
        main_post = query_to_dict(total_post)

        for post in main_post:
            post['current_status'] = get_current_status_name(post['status_id'])
            post['price'] = get_price_from_cost_negotiation(post['id'])
            post['worker'] = get_worker_from_post_id(post['id'])
            post['file_path'] = get_s3_path_from_post_id(post['id'])

        status_obj = get_status_obj("submitted_completed", "worker")
        workers = query_to_dict(db.session.query(
            User).filter(User.role_id == status_obj.id))


    return JSONResponse({
        "msg": "valid",
        'workers': workers,
        'main_jobs': main_post
    })


@user_router.post('/user/accpeted_job/')
async def post_data_job(request: Request,currentuser: UserModel = Depends(get_current_user)):
    data = await request.json()
    user_id = db.session.query(User).filter(
        User.email == currentuser.email).first()
    if user_id.role_id == 3:

        cost_obj = db.session.query(CostNegotiation).filter(
            CostNegotiation.job_id == data['job_id']).first()
        status_obj = get_status_obj("accepted", "cost")
        cost_obj.status_id = status_obj.id
        db.session.add(cost_obj)
        db.session.commit()

        status_obj = get_status_obj("submitted_waiting", "job")
        job_obj = db.session.query(Job).filter(
            Job.id == data['job_id']).first()
        job_obj.status_id = status_obj.id
        db.session.add(job_obj)
        db.session.commit()

    return JSONResponse(status_code=200)


@user_router.post('/user/reject_job/')
async def reject_job(request: Request,currentuser: UserModel = Depends(get_current_user)):
    data = await request.json()
    user_id = db.session.query(User).filter(
        User.email == currentuser.email).first()
    if user_id.role_id == 3:

        cost_obj = db.session.query(CostNegotiation).filter(
            CostNegotiation.job_id == data['job_id']).first()
        status_obj = get_status_obj("rejected", "cost")
        cost_obj.status_id = status_obj.id
        db.session.add(cost_obj)
        db.session.commit()

        status_obj = get_status_obj("rejected", "job")
        job_obj = db.session.query(Job).filter(
            Job.id == data['job_id']).first()
        job_obj.status_id = status_obj.id
        db.session.add(job_obj)
        db.session.commit()

    return JSONResponse(status_code=200)


@user_router.post('/user/superuser_valid/')
async def post_data_job(request: Request, currentuser: UserModel = Depends(get_current_user)):
    # data = await request.json()
    # decoded_id = decodeJWT(data['access_token'])
    if not currentuser:
        return JSONResponse(status_code=400, content={"msg": "invalid"})
    user_id = db.session.query(User).filter(
        User.email == currentuser.email).first()

    if user_id.role_id == 1:
        return JSONResponse(status_code=200, content={'msg': "valid"})
    else:
        return JSONResponse(status_code=400, content={'msg': "invalid", 'user_type': user_id.role_id})


@user_router.post('/user/get_type/')
async def get_user_type(request: Request):
    data = await request.json()
    decoded_id = decodeJWT(data['access_token'])
    user_id = db.session.query(User).filter(
        User.email == decoded_id['userID']).first()

    try:
        user_type = user_id.role_id
    except:
        user_type = 0

    return JSONResponse({"user_type": user_type})


@user_router.delete('/user/delete/{id}')
def delete_user(id: int):

    user_obj = db.session.query(User).filter(User.id == id)
    user_obj = user_obj.first()
    db.session.delete(user_obj)
    db.session.commit()
    return "Deleted"


@user_router.post('/user/reset_password/')
def user_reset_password(user: UserResetSchema, currentuser: UserModel = Depends(get_current_user)):
    print("+-++++++++++++",user)
    if not currentuser:
        return JSONResponse(status_code=400, content={"msg": "User is not valid"})
    user_obj = db.session.query(User).filter(
        User.email == currentuser.email)
    user_obj = user_obj.first()
    print(user_obj, user_obj.password)
    if not user_obj:
        return JSONResponse(status_code=400, content={"msg": "User is not valid"})
    if not Hasher.verify_password(user.old_password, user_obj.password):
        return JSONResponse(status_code=400, content={"msg": "User or Password is not valid"})

    user_obj.password = Hasher.get_password_hash(user.new_password)
    db.session.add(user_obj)
    db.session.commit()

    return JSONResponse(status_code=200)