"""

FaunaDB ORM

"""
from __future__ import annotations
from typing import Callable, List, Dict, Any, Union, Optional
from json import loads, dumps
from pydantic import BaseModel, BaseConfig, Field
from faunadb import query as q
from faunadb.client import FaunaClient
from faunadb.errors import FaunaError, NotFound, BadRequest
from kubernetes.config import process
from kubernetes.utils import log, uid



class FQLBaseModel(BaseModel):
    """Meta class for FQLModel"""
    id: Optional[str] = Field(default_factory=uid,unique=True)
    
    @classmethod
    def client(cls)->FaunaClient:
        """Return a FaunaDB client."""
        return FaunaClient(secret=process.env.FAUNA_SECRET)
    
    @classmethod
    def q(cls): # pylint: disable=invalid-name
        """Return the FaunaDB query object."""
        return cls.client().query
    
    @classmethod
    def provision(cls)->None:
        """Create the collection and indexes."""
        if not cls.q()(q.exists(q.collection(cls.__name__.lower()))):
            cls.q()(q.create_collection({"name": cls.__name__.lower()}))
            log(f"Created collection {cls.__name__.lower()}")
        for field in cls.__fields__.values():
            if field.field_info.extra.get("index"):
                index_data = {
                    "name": f"{cls.__name__.lower()}_by_{field.name}".lower(),
                    "source": q.collection(cls.__name__.lower()),
                    "terms": [{
                        "field": ["data", field.name]
                    }]
                }
                if cls.q()(q.exists(q.index(index_data["name"]))):
                    continue
                cls.q()(q.create_index(index_data))
                log(f"Created index {index_data['name']}")
                log(f"Created index {index_data['name']}")
            elif field.field_info.extra.get("unique"):
                index_data = {
                    "name": f"{cls.__name__.lower()}_unique_{field.name}".lower(),
                    "source": q.collection(cls.__name__.lower()),
                    "terms": [{
                        "field": ["data", field.name]
                    }],
                    "unique": True
                }
                if cls.q()(q.exists(q.index(index_data["name"]))):
                    continue
                cls.q()(q.create_index(index_data))
                log(f"Created index {index_data['name']}")
            elif field.field_info.extra.get("sort"):
                index_data = {
                    "name": f"{cls.__name__.lower()}_sort_{field.name}".lower(),
                    "source": q.collection(cls.__name__.lower()),
                    "values": [{
                        "field": ["data", field.name]
                    }]
                }
                if cls.q()(q.exists(q.index(index_data["name"]))):
                    continue
                cls.q()(q.create_index(index_data))
                log(f"Created index {index_data['name']}")
        if cls.q()(q.exists(q.index(f"{cls.__name__.lower()}_all".lower()))):
            return    
        cls.q()(q.create_index({
            "name": f"{cls.__name__.lower()}_all".lower(),
            "source": q.collection(cls.__name__.lower())
        }))
        log(f"Created index {cls.__name__.lower()}_all")
        return
    
    @classmethod
    def exists(cls, field: str, value: Any)->bool:
        """Check if a record exists in the database."""
        try:
            return cls.q()(q.exists(q.match(q.index(f"{cls.__name__}_by_{field}".lower()), value)))
        except FaunaError as e:
            log(e)
            return False

    @classmethod
    def find_unique(cls, field:str, value:Any)->Optional[Dict[str, Any]]:
        """Find a unique record in the database."""
        try:
            if cls.q()(q.exists(q.match(q.index(f"{cls.__name__}_unique_{field}".lower()), value))):
                return cls.q()(q.get(q.match(q.index(f"{cls.__name__}_unique_{field}".lower()), value)))
            else:
                return None
        except (NotFound, BadRequest) as e:
            log(e)
            return None
    
    @classmethod
    def find_many(cls, field: str, value: str, limit: int=100) -> List[Dict[str, Any]]:
        """
        
        Finds all the records that match the given field and value restricted by the limit
        
        """
        try:
            refs = cls.q()(q.paginate(q.match(q.index(f"{cls.__name__}_by_{field}".lower()), value), size=limit))
            return cls.q()(q.map_(lambda ref: q.get(ref), refs))
        except (NotFound, BadRequest,FaunaError) as e:
            return []
        
    @classmethod
    def sort(cls, field: str, direction: str, limit: int) -> List[Dict[str, Any]]:
        """
        
        Sorts the records in the collection by the given field and direction.
        
        """
        try:
            refs = cls.q()(q.paginate(q.sort(q.index(f"{cls.__name__}_sort_{field}".lower()), direction=direction), size=limit))
            return cls.q()(q.map_(lambda ref: q.get(ref), refs))
        except (NotFound, BadRequest,FaunaError) as e:
            return []
        
    @classmethod
    def delete(cls, field: str, value: str) -> bool:
        """
        
        Deletes one record from the collection with the given field and value.
        
        """
        try:
            response = cls.q()(q.get(q.match(q.index(f"{cls.__name__}_unique_{field}".lower()), value)))
            cls.q()(q.delete(response['ref']))
            return True
        except (NotFound, BadRequest,FaunaError) as e:
            log(e)
            return False
        
    @classmethod
    def find_all(cls, limit: int=100) -> List[Dict[str, Any]]:
        """
        
        Finds all the records in the collection.
        
        """
        try:
            refs = cls.q()(q.paginate(q.index(f"{cls.__name__}_all".lower()), size=limit))
            return cls.q()(q.map_(lambda ref: q.get(ref), refs))
        except (NotFound, BadRequest,FaunaError) as e:
            return []
        
    def instance_exists(self)->bool:
        """Check if the instance exists in the database."""
        for field in self.__fields__.values():
            if field.field_info.extra.get("unique"):
                if self.exists(field.name, getattr(self, field.name)):
                    return True
        return False

    def create(self)->Optional[Dict[str, Any]]:
        """Create a new record in the database."""
        if self.instance_exists():
            return None
        try:
            return self.q()(q.create(q.collection(self.__class__.__name__.lower()), {"data": self.dict()}))
        except FaunaError as e:
            log(e)
            return None
        
    def update(self)->Optional[Dict[str, Any]]:
        """Update an existing record in the database."""
        if not self.instance_exists():
            return None
        try:
           for field in self.__fields__.values():
                if field.field_info.extra.get("unique"):
                    return self.q()(q.update(q.get(q.match(q.index(f"{self.__class__.__name__}_unique_{field.name}".lower()), getattr(self, field.name))), {"data": self.dict()}))
        except FaunaError as e:
            log(e)
            return None
        
    
class FQLModel(FQLBaseModel):
    class Config(BaseConfig):
        orm_mode = True
        arbitrary_types_allowed = True