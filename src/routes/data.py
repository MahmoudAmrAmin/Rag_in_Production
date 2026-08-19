from fastapi import FastAPI , APIRouter , Depends ,UploadFile , status
from fastapi.responses import JSONResponse
from src.helpers import get_settings , Settings
from src.controllers import DataController , FileController , ProcessController 
from src.models import ResponseSignal
from .schemes.data import ProcessRequest 
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
@data_route.post('/upload/{folder_num}') 
async def upload_data(folder_num:str , file :UploadFile , app_settings:Settings = Depends(get_settings)) : 

    # validate file properties 
    is_valid , result_message = data_logic.validate_uploading_file(file=file)
    file_dir_path = file_logic.get_file_path( folder_num=folder_num)
    if not is_valid: 
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST , 
            content= { 
                'message' : result_message 
            }
        )
    file_path , gen_file_id = data_logic.generate_unique_file_path(
        ori_file_name= file.filename , 
        folder_num=folder_num
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
                        'message' : ResponseSignal.FILE_UPLOAD_FAILED.value  
                    }
                )


    
    return JSONResponse(
        status_code=status.HTTP_200_OK , 
        content={
             'message' : ResponseSignal.FILE_UPLOAD_SUCCESS.value , 
             'file_id' : gen_file_id  
        }
    )        

@data_route.post('/process/{folder_num}')  
async def process_file_endpoint(folder_num:str , process_request:ProcessRequest) : 
        file_id = process_request.file_id  
        chunk_size = process_request.chunk_size 
        overlap_size = process_request.overlap_size 
        do_reset = process_request.do_reset
        process_file_logic = ProcessController(file_id=file_id , folder_num=folder_num) 

        file_content = process_file_logic.get_file_content(file_id=file_id)
        file_chunks = process_file_logic.process_file_content(file_content=file_content,
                                                                file_id=file_id ,
                                                                chunk_size=chunk_size , 
                                                                overlap_size=overlap_size) 

        # check first if no problem in chunks 
        if file_chunks is None or len(file_chunks) == 0 : # so we have problem 
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST , 
                content= { 
                    'message' : ResponseSignal.PROCESSING_FAILED.value
                }
            )
        return file_chunks


