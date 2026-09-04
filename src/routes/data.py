from fastapi import FastAPI , APIRouter , Depends ,UploadFile , status , Request 
from fastapi.responses import JSONResponse
from src.helpers import get_settings , Settings
from src.controllers import DataController , FileController , ProcessController 
from src.models.enums.ResponseEnums import ResponseSignal
from src.models.database_schemes.data_chunk import DataChunk  
from .schemes.data import ProcessRequest  
from src.models.FileModel import FileModel 
from src.models.ChunkModel import ChunkModel 
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
@data_route.post('/upload/{project_id}') 
async def upload_data( request:Request , project_id:str , file :UploadFile ,
                       app_settings:Settings = Depends(get_settings) ) : 

    file_model = FileModel(
        db_clint=request.app.db_clint
    )
    project = await file_model.get_or_create_project(project_id=project_id)
    
    # validate file properties 
    is_valid , result_message = data_logic.validate_uploading_file(file=file)
    if not is_valid: 
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST , 
            content= { 
                'message' : result_message 
            }
        )
    project_dir_path = file_logic.get_file_path(project_id=project_id) 
    file_path , file_id = data_logic.generate_unique_file_path(
         ori_file_name=file.filename , 
         project_id=project_id

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
             'file_id' : file_id ,
        }
    )        





@data_route.post('/process/{project_id}')  
async def process_file_endpoint(request:Request , project_id:str , process_request:ProcessRequest) : 

        
        file_id = process_request.file_id  
        chunk_size = process_request.chunk_size 
        overlap_size = process_request.overlap_size 
        do_reset = process_request.do_reset 
        parse_process = ProcessController(project_id=project_id)

        file_content = parse_process.get_file_content(file_id=file_id)
        file_chunks = parse_process.process_file_content(file_content=file_content,
                                                                file_id=file_id ,
                                                                chunk_size=chunk_size , 
                                                                overlap_size=overlap_size) 

        file_model = FileModel(
            db_clint=request.app.db_clint
        )
        chunk_model = ChunkModel(
            db_clint=request.app.db_clint
        )

        project = await file_model.get_or_create_project(
            project_id=project_id
        )
       

        # check first if no problem in chunks 
        if file_chunks is None or len(file_chunks) == 0 : # so we have problem 
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST , 
                content= { 
                    'message' : ResponseSignal.PROCESSING_FAILED.value
                }
            )

        file_chunk_records = [ 
            DataChunk(
                chunk_text=chunk.page_content , 
                chunk_metadata=chunk.metadata , 
                chunk_order= i+1 ,
                chunk_file_id=project._id
            )
            for   i , chunk in enumerate(file_chunks)
        ]


        if do_reset == 1 : 
                _ = await chunk_model.delete_chunks_by_projec_id(project_id=project.id)
        

        num_records = await chunk_model.insert_many_chunks(chunks = file_chunk_records) 

        return JSONResponse(
            {
                'status' : ResponseSignal.PROCESSING_SUCCESS.value , 
                'inserted chunks': num_records     
            }
        )


