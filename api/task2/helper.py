from api.task2 import models
from common.common_functions import verify_password


def authenticate_user(email:str, password:str,db):
    user = db.query(models.Users).filter(models.Users.email == email ).first()
    if not user:
        return False

    if not verify_password(password,user.password):
        return False
    return user