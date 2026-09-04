from pydantic import BaseModel , Field , field_validator 
from typing import Optional 
from bson.objectid import ObjectId 


class DataChunk(BaseModel) : 
    """
        if we have attribute start with _ that mean its a private attribute and we 
        can't access it outside so the answer of this problem make alise name and remove the 
        ========>   _     <==========
    
    
    """
    id: Optional[ObjectId] = Field(None , alias='_id') 
    
    """
        we need to store order of each chunk 
        and those chunks related to which file
    
    """
    """
        Ellipsis sign (...)  means that field is required 
    
    """
    chunk_text : str = Field(... , min_length=1) 
    chunk_metadata:dict  
    chunk_order :int = Field(..., gt=0)
    chunk_file_id :ObjectId 


    class Config:
        arbitrary_types_allowed = True