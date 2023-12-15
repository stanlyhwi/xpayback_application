from sqlalchemy import  Column,String,BigInteger,Text
from config import BASE
import uuid

def default_uuid():
    return uuid.uuid4().hex

class Userdata(BASE):
    __tablename__="user_details1"
    user_id=Column(String(40), primary_key=True, default=lambda: default_uuid())
    email=Column(Text)
    full_name=Column(String(20),index=True)
    password = Column(Text)
    phone_no = Column(BigInteger)