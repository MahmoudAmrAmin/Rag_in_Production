from fastapi import FastAPI
from src.routes import base , data
from motor.motor_asyncio import AsyncIOMotorClient
from src.helpers.config import get_settings


async def lifespan(app:FastAPI) : 
    settings = get_settings() 
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_clint = app.mongo_conn[settings.MONGODB_DATABASE]
    print("MongoDB connection established")
    yield 
    app.mongo_conn.close() 
    print("MongoDB connection closed")

app = FastAPI(lifespan=lifespan)





app.include_router(base.base_router)
app.include_router(data.data_route) 
