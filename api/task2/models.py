from sqlalchemy import Boolean, Column , Integer ,String , ForeignKey,BigInteger,LargeBinary,Text
from sqlalchemy.orm import relationship
from config import BASE
import uuid

def default_uuid():
    return uuid.uuid4().hex

class Users(BASE):
    __tablename__ = "users"
    user_id=Column(String(40), primary_key=True, default=lambda: default_uuid())
    email=Column(String(50),unique=True,index=True)
    full_name=Column(String(50),index=True)
    password = Column(Text)
    phone_no = Column(BigInteger)
    
    profile = relationship("Profile",back_populates="user")


class Profile(BASE):
    __tablename__ = "profile"
    
    id = Column(String(40), primary_key=True, default=lambda: default_uuid())
    user_id=Column(String(40),ForeignKey('users.user_id'),unique=True)
    profile_picture=Column(Text)

    user = relationship("Users",back_populates="profile")