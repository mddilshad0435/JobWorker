from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from WebCore.models.base import Base
from WebCore.models.job import Job
from WebCore.models.user import User
from WebCore.models.status import Status


class WorkerJob(Base):
    __tablename__ = "worker_job"
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('job.id'))
    worker_id = Column(Integer, ForeignKey('user.id'))
    status_id = Column(Integer, ForeignKey('status.id'))
    job_repo_path = Column(String)

    job = relationship('Job')
    worker = relationship('User')
    status = relationship('Status')
