from kubernetes import create_app
'''from kubernetes.schemas.models import Issue, CodeFile, Project, MicroService, DataStore, User'''
from fastapi.staticfiles import StaticFiles
static = StaticFiles(directory="static", html=True)

app = create_app()

app.mount("/", static, name="static")

'''
@app.on_event("startup")
async def startup():
    Issue.provision()
    CodeFile.provision()
    Project.provision()
    MicroService.provision()
    DataStore.provision()
    User.provision()
'''