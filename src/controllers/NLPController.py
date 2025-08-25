from .BaseController import BaseController
from models.db_schemas import Project , DataChunck
from stores.llm.LLMEnum import DocumentTypeEnums
from typing import List
import json

class NLPController(BaseController):
    
    def __init__(self,vectordb_client , generation_client , embedding_client):
        
        super().__init__()

        self.vectordb_client = vectordb_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client

    def create_collection_name(self , project_id : str):
        return f"collection_{project_id}".strip()
    
    def reset_vectordb_collection(self , project : Project):

        collection_name = self.create_collection_name(project_id=project.project_id)
        self.vectordb_client.delete_collection(collection_name=collection_name)

    def get_vector_collection_info(self , project : Project):
    
        collection_name = self.create_collection_name(project_id = project.project_id)
        collection_info = self.vectordb_client.get_collection_info(collection_name = collection_name)
        return json.loads(json.dumps(collection_info,default=lambda x : x.__dict__))
    
    def index_into_vector_db(self , project : Project ,
                             chuncks : List[DataChunck] ,
                             chuncks_ids : List[int],
                             do_reset : bool = False):

        collection_name = self.create_collection_name(project_id= project.project_id)

        texts = [chunck.chunck_text for chunck in chuncks]
        metadatas = [chunck.chunck_metadata for chunck in chuncks]

        vectors = [
            self.embedding_client.embed_text(text = text, document_type=DocumentTypeEnums.DOCUMENT.value)
            for text in texts
        ]


        _ = self.vectordb_client.create_collection(collection_name = collection_name , embedding_size = self.embedding_client.embedding_size, do_reset = do_reset)


        self.vectordb_client.insert_many(collection_name = collection_name , texts = texts , metadata = metadatas , vectors = vectors , record_ids = chuncks_ids)

        return True

    def search_vector_db_collection(self , project : Project , text : str , limit : int = 100):

        collection_name = self.create_collection_name(project_id= project.project_id)
        print(collection_name)

        vector = self.embedding_client.embed_text(text , document_type = DocumentTypeEnums.QUERY.value)

        if not vector or len(vector) == 0:
            return False
        
        results = self.vectordb_client.search_by_vector(
            collection_name = collection_name,
            vector = vector,
            limit = limit
        )

        if not results:
            return False

        return json.loads(
            json.dumps(results , default = lambda x : x.__dict__)
        )