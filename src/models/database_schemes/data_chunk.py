from pydantic import BaseModel , Field , field_validator 
from typing import Optional 
from bson.objectid import ObjectId 


class DataChunk(BaseModel) : 

    _id: Optional[ObjectId] 
    
    """
        we need to store order of each chunk 
        and those chunks related to which file
    
    """

    chunk_text : str = Field(... , min_length=1) 
    chunk_metadata:dict  
    chunk_order :int = Field(..., gt=0)
    chunk_file_id :ObjectId 


    class Config: 
        arbitrary_types_allowed = True 
