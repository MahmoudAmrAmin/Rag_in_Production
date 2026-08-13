from fastapi import FastAPI , APIRouter
from dotenv import load_dotenv , find_dotenv
import os 
base_router = APIRouter(
    # prefix paramters give all endpoint same prefix of path
    prefix='/api/v1' , 
    # compain many endpoint under tags 
    tags=['api_v1']
)

@base_router.get("/") 
async def welcome():
    app_name = os.getenv('APP_NAME')
    app_version = os.getenv('APP_VERSION')

    return {
        'app name' : app_name , 
        'app version' : app_version
    }
