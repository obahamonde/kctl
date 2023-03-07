from typing import List, Optional
from pydantic import Field
from kubernetes.services.orm import FQLModel as Q
from kubernetes.config import process
from kubernetes.utils import (
    get_time,
    get_id,
    get_name,
    get_password,
    get_port,
    get_host,
)



class User(Q):
    sub: str = Field(...,unique=True)
    name: str = Field(...)
    email: Optional[str] = Field(default=None,index=True)
    picture: Optional[str] = Field(default=None)
    nickname: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default_factory=get_time,index=True)
    email_verified: Optional[bool] = Field(default=False,index=True)
    given_name: Optional[str] = Field(default=None)
    family_name: Optional[str] = Field(default=None)
    locale: Optional[str] = Field(default=None,index=True)


class Issue(Q):
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default="open",index=True)
    labels: Optional[List[str]] = Field(default=[],index=True)
    completed: Optional[bool] = Field(default=False,index=True)
    project: Optional[str] = Field(default=None,index=True)
    last_modified: Optional[str] = Field(default_factory=get_time,index=True)
    owner: Optional[str] = Field(default=None,index=True)


class CodeFile(Q):
    name: Optional[str] = Field(default=None)
    content: Optional[str] = Field(default=None)
    project: Optional[str] = Field(default=None)
    last_modified: Optional[str] = Field(default_factory=get_time,index=True)
    url: Optional[str] = Field(default=None, index=True)
    icon: Optional[str] = Field(default=None)
    content_type: Optional[str] = Field(default=None,index=True)
    size: Optional[float] = Field(default=None,index=True)
    extension: Optional[str] = Field(default=None,index=True)
    owner: Optional[str] = Field(default=None,index=True)


class Project(Q):
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    last_modified: Optional[str] = Field(default_factory=get_time)
    code_files: Optional[List[CodeFile]] = Field(default_factory=list)
    issues: Optional[List[Issue]] = Field(default_factory=list)
    owner: Optional[str] = Field(default=None)


class MicroService(Q):
    name: Optional[str] = Field(default=None)
    runtime: Optional[str] = Field(default=None,index=True)
    function_name: Optional[str] = Field(default=None)
    code: Optional[List[CodeFile]] = Field(default_factory=list)
    zip: Optional[bytes] = Field(default=None)
    zip_url: Optional[str] = Field(default=None)
    function_url: Optional[str] = Field(default=None)
    function_id: Optional[str] = Field(default_factory=get_id)
    function_arn: Optional[str] = Field(default=None)
    owner: Optional[str] = Field(default=None,index=True)


class DataStore(Q):
    image: str = Field(...,index=True)
    protocol: str = Field(default="tcp")
    name: str = Field(default_factory=get_name,index=True)
    host: str = Field(default_factory=get_host)
    host_port: int = Field(default_factory=get_port)
    username: str = Field(default_factory=get_name)
    password: str = Field(default_factory=get_password)
    database: Optional[str] = Field(default_factory=get_name)
    container_id: Optional[str] = Field(default=None)
    database_uri: Optional[str] = Field(default=None)
    container_port: Optional[int] = Field(default=None)
    owner: Optional[str] = Field(default=None,index=True)
