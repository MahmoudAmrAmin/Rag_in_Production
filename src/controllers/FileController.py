from .BaseController import BaseController 
from fastapi import UploadFile 
from src.models import ResponseSignal
import os 


class FileController(BaseController): 
    def __init__(self):
        super().__init__()

    def get_file_path(self , folder_num:str) : 
        file_dir =   os.path.join(
            self.file_dir , 
            folder_num
        )       

        if not os.path.exists(file_dir): 
            os.makedirs(file_dir) 
        return file_dir    