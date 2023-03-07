from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from kubernetes.services.docker import DockerService
from kubernetes.schemas.models import DataStore
from kubernetes.utils import log


class DataStoreResource(APIRouter):
    """Database as a Service"""
    def __init__(self):
        super().__init__()
        self.prefix = "/datastores"

        @self.get("/")
        def index():
            response = DataStore.find_all(100)
            log(response)
            
        @self.get("/")
        def list_(sub: str):
            response =  DataStore.find_many("owner", sub)
            log(response)

        @self.post("/{image}")
        async def create(image: str,sub:str ):
            data = await DockerService(image=image).run()
            data_store = DataStore(**data.dict())
            data_store.owner = sub
            data_in_db = DataStore(**data_store.dict())
            response = data_in_db.create()
            return response["data"]
        
        @self.get("/{name}")
        async def read(name: str):
            return await DockerService.get(name=name)

        @self.delete("/{name}")
        async def delete(name: str):
            response = await DockerService.stop(name=name)
            log(response)
            response = await DockerService.delete(name=name)
            log(response)
            response = DataStore.delete("name", name)
            log(response)