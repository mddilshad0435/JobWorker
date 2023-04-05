from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from WebCore.models.base import Base


class Job(Base):
    __tablename__ = "job"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('user.id'))
    title = Column(String)
    description = Column(String)
    job_file_path = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    status_id = Column(Integer, ForeignKey('status.id'))
    is_active = Column(Boolean, default=True)

    status = relationship("Status")
    customer = relationship("User")
