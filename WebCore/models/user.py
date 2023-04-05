from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship, backref
from WebCore.models.base import Base
from WebCore.models.role import Role


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50))
    password = Column(String(200))
    username = Column(String(30))
    mobile = Column(Integer)
    bio = Column(Text)
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey('role.id'))
    role = relationship('Role')
    # address = relationship('Address', backref=backref("user", uselist=False))


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    country_id = Column(Integer)
    # country_name = Column(String(70))
    state_id = Column(Integer)
    # state_name = Column(String(100))
    city_id = Column(Integer)
    # city_name = Column(String(100))
    zipCode = Column(Integer)
    address1 = Column(Text)
    address2 = Column(Text)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship('User', uselist=False)