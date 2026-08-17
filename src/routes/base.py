from fastapi import FastAPI , APIRouter , Depends
from src.helpers.config import get_settings ,Settings
base_router = APIRouter(
    # prefix paramters give all endpoint same prefix of path
    prefix='/api/v1' , 
    # compain many endpoint under tags 
    tags=['api_v1']
)

setting_config = get_settings()

@base_router.get("/") 
async def welcome(app_settings:Settings = Depends(get_settings)): 
    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION 
    return {
        'app name' : app_name , 
        'app version' : app_version
    }
