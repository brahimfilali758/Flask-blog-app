import os
from dotenv import load_dotenv # just to load the environements variables

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    MAIL_SERVER =  'smtp.gmail.com'
    MAIL_PORT   =  465
    MAIL_USE_TLS =  False
    MAIL_USE_SSL =  True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
