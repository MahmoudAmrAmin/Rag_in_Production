from fastapi import FastAPI
from dotenv import load_dotenv , find_dotenv
dot_env_path = find_dotenv()
load_dotenv(dot_env_path)


from routes import base
app = FastAPI()
app.include_router(base.base_router)