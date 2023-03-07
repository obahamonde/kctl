from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from kubernetes.routers import Router


class App(FastAPI):
    def __init__(self):
        super().__init__()
        self.include_router(Router())
        