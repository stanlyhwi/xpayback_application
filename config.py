from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pymongo import MongoClient
# from pickle import FALSE

import os
load_dotenv()

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

ENGINE = create_engine(SQLALCHEMY_DATABASE_URI)

SESSIONLOCAL = sessionmaker(autocommit=False,autoflush=False ,bind = ENGINE)

BASE = declarative_base()

CLIENT = MongoClient(os.getenv('MONGO_DATABASE_URI'))
DBM = CLIENT[os.getenv('MONGO_DATABASE_NAME')]
COLLECTION = DBM[os.getenv('MONGO_COLLECTION_NAME')]


UPLOAD_FILE_FOLDER = os.getenv('UPLOAD_FOLDER')

if not os.path.exists(UPLOAD_FILE_FOLDER):
    os.makedirs(UPLOAD_FILE_FOLDER)