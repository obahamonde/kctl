from fastapi import APIRouter, HTTPException, Body
from kubernetes.schemas.models import Issue
from kubernetes.schemas.schemas import IssueSchema, loads

class IssueResource(APIRouter):
    """Issues Resource
    """

    def __init__(self):
        super().__init__()
        self.prefix = "/issues"

        
        @self.get("/{sub}")
        async def list_issues_by_subscriptor(sub: str):
            """return Issue.find_many("sub", sub, 100)"""
            return Issue.find_many("owner",sub, 100)


        @self.post("/")
        async def create_issue_instance(issue=Body(...)):
            try:
                issue = Issue(**loads(issue))
                return issue.create()
            except Exception as exc:
                raise HTTPException(status_code=500, detail=str(exc)) from exc

        @self.put("/")
        async def update_issue_by_id(id: str, body=Body(...)):
            try:
                issue = Issue(**loads(body))
                return issue.update("id", id, issue.dict())
            except Exception as exc:
                raise HTTPException(status_code=500, detail=str(exc)) from exc
        
        @self.delete("/{id}")
        async def delete_issue_by_id(id: str):
            try:
                Issue.delete("id", id)
            except Exception as exc:
                raise HTTPException(status_code=500, detail=str(exc)) from exc