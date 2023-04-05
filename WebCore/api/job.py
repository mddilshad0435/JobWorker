import datetime
import os

from fastapi import Request, Depends,Response, Form
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi_sqlalchemy import db

from WebCore.auth.jwt_handler import decodeJWT
from WebCore.auth.oauth2 import get_current_user
from WebCore.api.base import get_status_obj
from WebCore.models.user import User
from WebCore.models.job import Job
from WebCore.uploading_file.main import upload_to_aws, download_from_aws,download_file_obj
from WebCore.models.role import Role
from WebCore.models.status import Status
from WebCore.models.cost_negotitation import CostNegotiation
from WebCore.models.worker_job import WorkerJob
from WebCore.schemas.request.user import UserModel
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from dotenv import load_dotenv

load_dotenv('.env')

job_router = APIRouter()


async def save_file(file_path, file):
    with open(file_path, 'wb') as f:
        f.write(await file.read())


@job_router.post('/create_job/')
async def post_data_job(request: Request, currentuser: UserModel = Depends(get_current_user)):

    data = await request.form()
    current_date_time = datetime.datetime.now()

    user_id = db.session.query(User).filter(
        User.email == currentuser.email).first()

    job_file_path = 'static/files/'+user_id.username + \
        "_"+str(current_date_time) + data['file'].filename
    role_obj = db.session.query(Role).filter(Role.name=="customer").first()
    if user_id.role_id == role_obj.id:
        await save_file(job_file_path, data['file'])
        # status_obj = db.session.query(Status).filter(Status.name=="started",Status.category=="job").first()
        status_obj = get_status_obj("started", "job")
        print(status_obj.id)
        db_job = Job(
            customer_id=user_id.id,
            title=data['title'],
            description=data['description'],
            job_file_path=job_file_path,
            status_id=status_obj.id
        )
        db.session.add(db_job)
        db.session.commit()

    return JSONResponse(status_code=200)


@job_router.post('/job/update_price/')
async def post_data_job(request: Request, currentuser: UserModel = Depends(get_current_user)):

    data = await request.json()

    user_id = db.session.query(User).filter(
        User.email == currentuser.email).first()
    role_obj = db.session.query(Role).filter(Role.name=="superuser").first()
    if user_id.role_id == role_obj.id:
        status_obj = get_status_obj("pending", "cost")
        cost_obj = CostNegotiation(
            admin_id=user_id.id,
            cost=data['price'],
            job_id=data['job_id'],
            status_id=status_obj.id
        )
        db.session.add(cost_obj)
        db.session.commit()
        status_obj = get_status_obj("submitted_and_price_quoted", "job")
        job_obj = db.session.query(Job).filter(Job.id == data['job_id'])
        job_obj = job_obj.first()
        job_obj.status_id = status_obj.id
        db.session.add(job_obj)
        db.session.commit()

    return JSONResponse(status_code=200)


@job_router.post('/job/assign_to/')
async def post_data_job(request: Request, currentuser: UserModel = Depends(get_current_user)):

    data = await request.json()

    user_id = db.session.query(User).filter(
        User.email == currentuser.email).first()
    role_obj = db.session.query(Role).filter(Role.name=="superuser").first()
    if user_id.role_id == role_obj.id:
        status_obj = get_status_obj("submitted_processing", "worker")
        worker_obj = WorkerJob(
            job_id=data['job_id'],
            worker_id=data['worker_id'],
            status_id=status_obj.id,
        )
        db.session.add(worker_obj)
        db.session.commit()
        db.session.refresh(worker_obj)

        status_obj = get_status_obj("submitted_processing", "job")

        job_obj = db.session.query(Job).filter(
            Job.id == data['job_id']).first()
        job_obj.status_id = status_obj.id
        db.session.add(job_obj)
        db.session.commit()
        db.session.refresh(job_obj)

    return JSONResponse(status_code=200)


@job_router.post('/job/complete/')
async def post_data_job(request: Request, currentuser: UserModel = Depends(get_current_user)):

    data = await request.json()

    user_id = db.session.query(User).filter(
        User.email == currentuser.email).first()
    role_obj = db.session.query(Role).filter(Role.name=="worker").first()
    if user_id.role_id == role_obj.id:
        status_obj = get_status_obj("submitted_completed", "worker")
        worker_job_obj = db.session.query(WorkerJob).filter(
            WorkerJob.id == data['worker_job_id']).first()
        job_obj = db.session.query(Job).filter(
            Job.id == worker_job_obj.job_id).first()
       
        file_name = job_obj.job_file_path.split('/')[-1]
        print(file_name, user_id.username+"/"+file_name, os.environ['BUCKET_NAME'], job_obj.job_file_path)
        print(type(file_name), type(user_id.username+"/"+file_name), type(os.environ['BUCKET_NAME']), type(job_obj.job_file_path))
        s3_file_path, msg = upload_to_aws(job_obj.job_file_path, os.environ['BUCKET_NAME'], user_id.username+"/"+file_name)
        if not s3_file_path:
            return JSONResponse(status_code=400, content=msg)

        worker_job_obj.status_id = status_obj.id
        
        worker_job_obj.job_repo_path = s3_file_path
        db.session.add(worker_job_obj)
        db.session.commit()

        status_obj = get_status_obj("submitted_completed", "job")
        
        job_obj.status_id = status_obj.id
        db.session.add(job_obj)
        db.session.commit()

    return JSONResponse(status_code=200)


# @job_router.post('/job/download_file/')
# async def download_file(request: Request, currentuser: UserModel = Depends(get_current_user)):
#     data = await request.json()

#     user_id = db.session.query(User).filter(
#         User.email == currentuser.email).first()
#     if user_id:
#         job_obj = db.session.query(Job).filter(Job.id==data['job_id']).first()
#         file_name = job_obj.job_file_path.split('/')[-1]
#         from pathlib import Path
#         # downloads_path = str(Path.home() / "Downloads")
#         # file_name = downloads_path+'/'+file_name
#         print("--------------",file_name)
#         worker_job_object = db.session.query(WorkerJob).filter(WorkerJob.job_id==data['job_id']).first()
#         res, msg = download_from_aws(os.environ['BUCKET_NAME'], worker_job_object.job_repo_path, file_name)
#         if res:
#             return FileResponse(path=file_name, filename=file_name)
#             # return JSONResponse(status_code=200, content=msg)
#         else:
#             return JSONResponse(status_code=400, content=msg)
#     return JSONResponse(status_code=400, content={"msg": "Invalid user"})


@job_router.post('/job/file_download/')
async def job_download_file(jobid: int = Form(...),currentuser: UserModel = Depends(get_current_user)):
    print(jobid)
    user_id = db.session.query(User).filter(
        User.email == currentuser.email).first()
    if user_id:
        job_obj = db.session.query(Job).filter(Job.id==jobid).first()
        file_name = job_obj.job_file_path.split('/')[-1]
        worker_job_object = db.session.query(WorkerJob).filter(WorkerJob.job_id==jobid).first()

        file = download_file_obj(os.environ['BUCKET_NAME'], worker_job_object.job_repo_path,file_name)
        if file is not None:
            return Response(
                file['Body'].read(),
                headers={"Content-Disposition": f"attachment;filename={file_name}"}
            )
        else:
            print("Not able to download file")