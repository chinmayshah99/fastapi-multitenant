from contextlib import asynccontextmanager
import importlib

from fastapi import FastAPI

from database import engine
from routers.user import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # dynamically import models from tenants
    for tenant in ['tenant_a', 'tenant_b']:
        module = importlib.import_module(f"tenants.{tenant}.models")
        Base = getattr(module, 'Base')
        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan, title="FastAPI Multi Tenant")
app.include_router(user_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
