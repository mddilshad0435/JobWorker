from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from WebCore.models.base import Base
from WebCore.models.user import User
from WebCore.models.status import Status

# Base = declarative_base()


class CostNegotiation(Base):
    __tablename__ = "cost_negotiation"
    id = Column(Integer, primary_key=True)
    admin_id = Column(Integer, ForeignKey('user.id'))
    cost = Column(Integer)
    job_id = Column(Integer, ForeignKey('job.id'))
    status_id = Column(Integer, ForeignKey('status.id'))
    admin = relationship('User')
    status = relationship('Status')
