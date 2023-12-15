from common.common_functions import get_db,get_password_hash
from fastapi import Depends,APIRouter,Form,File,UploadFile
from api.task1.helper import authenticate_user
from common.response import success,failure
from common.db_interactions import add_data
from sqlalchemy.orm import Session
from config import COLLECTION,UPLOAD_FILE_FOLDER
from api.task1 import models
from config import ENGINE
import traceback
import os



models.BASE.metadata.create_all(bind=ENGINE)


router = APIRouter(
    prefix="/task1",
    tags=["task1"],
    responses={404:{"description":"not found"}}
)


@router.post("/register")
async def register_user(payload:dict,db:Session = Depends(get_db)):
    try:

        email_check=db.query(models.Userdata).filter(models.Userdata.email==payload["email"]).first()
        
        if email_check:
            return failure("Email already exist")

        user_model = models.Userdata()
        user_model.full_name = payload["full_name"]
        user_model.email = payload["email"]
        user_model.phone_no = payload["phone_no"]
        hash_password = get_password_hash(payload["password"])
        user_model.password = hash_password

        if not add_data(user_model,db):
            return failure("an error occured while storing the data")

        return success("User registered successfully use this user_id to upload profile_picture",{"user_id":user_model.user_id})
    
    except Exception as err:
        traceback.print_exc()
        return failure("an error occured")
    

@router.post("/upload_image_file")
async def upload_image_file(
    user_id: str = Form(...),
    image_file: UploadFile = File(...),
    db:Session = Depends(get_db)
    ):
    try:
        
        if image_file.filename == "":
            return failure("please send the file in request body")

        allowed_extensions = {'jpg', 'jpeg', 'png'}
        file_extension = image_file.filename.split('.')[-1].lower()

        if file_extension not in allowed_extensions:
            return failure("Only jpg or png or jpeg files are allowed for upload")

        valid_user_id = db.query(models.Userdata).filter(models.Userdata.user_id==user_id).first()

        if not valid_user_id :
            return failure("invalid user_id please use the correct user_id , user_id provided while user registration")

        existing_user = COLLECTION.find_one({"user_id": user_id})
        if existing_user:
            return failure("Image already exist for user, cant upload new image")
        
        contents = await image_file.read()
        filename = f"{user_id}_{image_file.filename}"
        filepath = os.path.join(UPLOAD_FILE_FOLDER, filename)

        with open(filepath, "wb") as f:
            f.write(contents)
        
        result = COLLECTION.insert_one({
            "user_id": user_id,
            "file_name": filename,
            "profile_image": filepath
        })
        
        if not result:
            return failure("An error occured while storing the data")

        return success("Image file uploaded successfully", [])

    except Exception as err:
        traceback.print_exc()
        return failure("An error occurred")
    

@router.get("/login")
async def login(payload: dict, db: Session = Depends(get_db)):

    try:
        if "password" not in payload:
            return failure("password key missing in payload")
        if "email" not in payload:
            return failure("email key missing in payload")

        user = authenticate_user(payload["email"], payload["password"], db)

        if not user:
            return failure("username or password is invalid")

        result = []
        data = {}

        stored_image_data = COLLECTION.find_one({"user_id": user.user_id})

        if not stored_image_data:
            return failure("profile image not uploaded, kindly upload and try again")

        image_path = stored_image_data.get("profile_image")

        if not image_path:
            return failure("error while fetching the image path")

        data["Email"] = user.email
        data["Phone Number"] = user.phone_no
        data["Full Name"] = user.full_name
        data["Profile Image"] = image_path

        result.append(data)

        return success("success", result)

    except Exception as err:
        traceback.print_exc()
        return failure("an error occurred")