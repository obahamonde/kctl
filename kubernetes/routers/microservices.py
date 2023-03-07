from json import loads
from fastapi import APIRouter, Body, HTTPException
from kubernetes.schemas.models import MicroService
from kubernetes.schemas.schemas import MicroServiceSchema
from kubernetes.services.aws import create_microservice


class MicroServiceResource(APIRouter):
    def __init__(self):
        super().__init__()
        self.prefix = "/microservices"

        @self.post("/")
        async def deploy_microservice(microservice=Body(...)):
            payload = loads(microservice)
            microservice = MicroService(**payload)
            if MicroService.find_unique("name", microservice.name):
                raise HTTPException(
                    status_code=400, detail="Microservice name already exists"
                )
            function_data = await create_microservice(
                microservice.name, microservice.code
            )
            microservice.function_arn = function_data["function_arn"]
            microservice.function_name = function_data["function_name"]
            microservice.function_url = function_data["function_url"]
            microservice_in_db = MicroService(**microservice.dict())
            return microservice_in_db.create()
