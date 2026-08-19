import os 
from .BaseController import BaseController 
from .FileController import FileController 
from src.models  import ProcessingEnum 
from langchain_community.document_loaders  import TextLoader 
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class ProcessController(BaseController) : 
    def __init__(self , folder_num:str , file_id :str):
        super().__init__()
        self.file_id = file_id 
        self.folder_path = FileController().get_file_path(folder_num=folder_num) 
        self.file_path = os.path.join(
            self.folder_path , 
            file_id
        )


    def get_file_extention(self , file_id :str) :
        return os.path.splitext(file_id)[-1].lower()


    def get_file_loader(self , file_id:str) : 
        file_ext = self.get_file_extention(file_id=file_id) 
        file_path = self.file_path
        """ 
            # if error occur 
            file_path = os.path.join( 
                self.file_path , 
                file_id 
            )
        
        """
        if file_ext == ProcessingEnum.TXT.value : 
            # that Textloader need also file path
            return TextLoader(file_path=file_path , encoding='utf-8') 
        if file_ext == ProcessingEnum.PDF.value : 
            return PyMuPDFLoader(file_path=file_path)  
        if file_ext == ProcessingEnum.DOCX.value: 
            return Docx2txtLoader(file_path=file_path)
        raise ValueError(f"Unsupported or missing file extension: '{file_ext}' for file_id: '{file_id}'")
        return None
    
    def get_file_content(self ,file_id:str ): 

        loader = self.get_file_loader(file_id=file_id) 
        return loader.load()
    
    def process_file_content(self , file_content:list ,file_id:str, chunk_size:int = 100 , overlap_size:int= 100):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size , 
            chunk_overlap = overlap_size , 
            length_function = len
        ) 

        """
        because file_content is list contain file content of document and metadata 
        and we need meta data so we need to extract from this list just file content by list comprehension
        """
        file_content_text = [
            text.page_content for text in file_content
        ]
        file_metadata =  [
            text.metadata for text in file_content
        ]
        chunks = text_splitter.create_documents(
            file_content_text , 
            metadatas=file_metadata
        )

        return chunks