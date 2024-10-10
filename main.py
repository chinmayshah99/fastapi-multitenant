from contextlib import asynccontextmanager
import importlib

from fastapi import FastAPI

from database import engine, get_db
from routers.user import router as user_router
from controllers.user.base_user import BaseUser
from utils import map_domain_to_class


@asynccontextmanager
async def lifespan(app: FastAPI):
    # dynamically import models from tenants
    for tenant in ['tenant_a', 'tenant_b']:
        module = importlib.import_module(f"tenants.{tenant}.models")
        Base = getattr(module, 'Base')
        Base.metadata.create_all(bind=engine)

        # create a user for each tenant
        # note not needed in production; just for testing
        user = module.User(email=f"admin@{tenant}.com", name=f"Admin {tenant}", is_active=True)
        domain_mapping = map_domain_to_class("user", BaseUser)
        user_object = domain_mapping[tenant]
        user_object.create_user(next(get_db()), user = user)
    yield


app = FastAPI(lifespan=lifespan, title="FastAPI Multi Tenant")
app.include_router(user_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
