"""CodeFile Resource"""
from json import loads
from fastapi import APIRouter, Body, HTTPException
from kubernetes.schemas.models import CodeFile
from kubernetes.schemas.schemas import CodeFileSchema


class CodeFileResource(APIRouter):
    """IDE as a Service"""
    def __init__(self):
        super().__init__()
        self.prefix = "/codefiles"

        @self.get("/")
        async def index(sub: str):
            return CodeFile.find_many("owner", sub,32)

        @self.post("/")
        async def create(sub: str, codefile=Body(...)):
            codefile_schema = CodeFile(**loads(codefile))
            codefile_schema.owner = sub
            return codefile_schema.create()

        @self.delete("/{url}")
        async def delete(url: str):
            CodeFile.delete("url", url)