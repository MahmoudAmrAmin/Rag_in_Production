from fastapi import FastAPI , APIRouter , Depends ,UploadFile , status
from fastapi.responses import JSONResponse
from src.helpers import get_settings , Settings
from src.controllers import DataController
from src.controllers import FileController
import os 
import aiofiles
import logging

logger = logging.getLogger('uvicorn.error') 

data_route = APIRouter(
    prefix='/api/v1/data' , 
    tags=['api_v1' , 'data']
) 

data_logic = DataController()
file_logic = FileController()

# upload endpoint in data route
@data_route.post('/upload/{file_id}') 
async def upload_data(file_id:str , file :UploadFile , app_settings:Settings = Depends(get_settings)) : 

    # vaildate file properties 
    is_vaild , result_message = data_logic.vaildate_uploading_file(file=file)
    file_dir_path = file_logic.get_file_path(file_id = file_id)
    if not is_vaild: 
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST , 
            content= { 
                'message' : result_message 
            }
        )
    file_path = data_logic.generate_unique_filename(
        ori_file_name= file.filename , 
        file_id=file_id
    )
    try : 
        async with aiofiles.open(file_path , 'wb') as f : 
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE): 
                await f.write(chunk) 
    except Exception as e :

            logger.error(f'Error While uploading file : {e}')
            return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST , 
                    content= { 
                        'message' : result_message 
                    }
                )
    return JSONResponse(
        status_code=status.HTTP_200_OK , 
        content=result_message
    )               