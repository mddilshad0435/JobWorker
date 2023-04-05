from sqlalchemy import Column, Integer, String, Boolean
from WebCore.models.base import Base


class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    is_active = Column(Boolean, default=True)


# 1=Superuser
# 2=Worker
# 3=Customer
