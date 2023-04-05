from sqlalchemy import Column, Integer, String, Boolean
from WebCore.models.base import Base


class Status(Base):
    __tablename__ = "status"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    category = Column(String(50))
    is_active = Column(Boolean, default=True)


# 1 Processing
# 2 Completed
# 3 Approved
# 4 Pending
# 5 Rejected
# 6 Waiting for approval
