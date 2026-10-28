from fastapi import FastAPI

from .auth import router

app = FastAPI(title="Authentication Service")
app.include_router(router)