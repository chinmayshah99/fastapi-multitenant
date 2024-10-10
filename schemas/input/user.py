from pydantic import BaseModel


class BaseUserCreate(BaseModel):
    email: str
    name: str
    is_active: bool
