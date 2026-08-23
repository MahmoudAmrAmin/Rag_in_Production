from pydantic import BaseModel ,Field,field_validator  
from typing import Optional 
from bson.objectid import ObjectId 
class File(BaseModel) : 
    _id: Optional[ObjectId] 
    file_id : str =Field(... , min_length=1)



    # make manual validation 
    @field_validator('file_id') 
    def vaildate_file_id(cls , user_value) : 
        if not user_value.isalnum(): 
            raise ValueError('file id numst be alphanumeric')
        return user_value 


    # to make the validation system understand objectId type (because its not support in pydantic) 

    class Config: 
        arbitrary_types_allowed = True 