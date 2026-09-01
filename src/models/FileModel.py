from .BaseDataModel import BaseDataModel
from .database_schemes import  File
from .enums import DataBaseEnum 

class FileModel(BaseDataModel): 
    def __init__(self, db_clint:object):
        super().__init__(db_clint) 
        self.collection = self.db_clint[DataBaseEnum.COLLECTION_FILE_NAME.value]


    async def insert_file(self ,file:File ) : 
        result = await self.collection.insert_one(file.model_dump())    
        file._id = result.inserted_id  

        return file 

    async def get_or_create_file(self , file_id :str) : 
        record = await self.collection.find_one({
            'file_id' :file_id
        }) 

        if record is None :  
            # if not exist will create it 
            file = File(file_id=file_id) 
            file = await self.insert_file(file=file) 

            return file 
        return File(**record) 
    
    
    async def get_all_file(self ,page:int = 1 , page_size :int = 10  ) : 
        """
            the function of get all files is Critical and sensitive functions because its  kill performance.
            So we must use pagination with it 
        """ 
        # so first we need to know number of files in my collection 

        total_docs = await self.collection.count_documents({}) # in practs we leave condition and if empty it will count every thing 
        total_pages = total_docs // page_size 
        if total_docs % page_size != 0:  
            total_pages+=1 

        # now will collect data 
        cursor = self.collection.find().skip((page -1 ) * page_size).limit(page_size) # cursor will return records as dict 

        projects = [] 
        async for document in cursor: 
            projects.append( 
                # so here we need convert dict (documents) to File Data Model 
                File(**document)
            ) 
        return projects , total_pages      
        