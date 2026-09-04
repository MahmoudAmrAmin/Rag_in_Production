from .BaseController import BaseController
from fastapi import UploadFile 
from src.models import ResponseSignal
from .BaseController import BaseController 
from .FileController import FileController
import re 
import os 

file_logic  = FileController()
class DataController(BaseController): 
   def __init__(self):
      super().__init__()
      self.size_scale = (1024 * 1024) # convert from MB to Bytes 
   
   # start validating uploading file 
   def validate_uploading_file(self , file:UploadFile):   

       # we need check if type of file is valid 
      if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES: 
        
         return False , ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
      
      if file.size > (self.app_settings.FILE_MAX_SIZE * self.size_scale) : 
         """
            file.size:Attribute return size in Byte But we set validation in MGByte
         
         """
         return False ,ResponseSignal.FILE_SIZE_EXCEEDED.value
      
      return True  ,ResponseSignal.FILE_UPLOAD_SUCCESS.value 

   
   def generate_unique_file_path(self , ori_file_name: str ,project_id:str ) : 
      rand_key = self.generate_random_string()

      file_path = file_logic.get_file_path(project_id=project_id) 

      clean_filename = self.get_clean_filename(ori_filename=ori_file_name)

      new_file_path = os.path.join(
         file_path , 
         rand_key + '_' + clean_filename
      ) 

      while os.path.exists(new_file_path) : 
         rand_key = self.generate_random_string()
         new_file_path = os.path.join(
               file_path , 
               rand_key + '_' + clean_filename
         )
         
      new_name = rand_key + '_' + clean_filename    
      return new_file_path   , new_name 

   def get_clean_filename(self , ori_filename:str) : 
      clean_filename = re.sub(r'[^\w.]' ,'' , ori_filename.strip()) 

      clean_filename = clean_filename.replace(" " , '_') 

      return clean_filename 