from sqlalchemy.orm import Session

from schemas import ResponseModel
from schemas.input.user import BaseUserCreate
from schemas.output.user import BaseUserDisplay
from utils import dynamic_import_module


class BaseUser:
    def __init__(self, domain: str = None):
        self.domain = domain
        self.models = dynamic_import_module(domain)

    def get_all_users(self, db: Session):
        users = db.query(self.models.User).all()
        users_data = [BaseUserDisplay.from_orm(user) for user in users]
        return ResponseModel(
            data={"users": users_data}, message="Users fetched successfully", error=None
        )
    
    def create_user(self, db: Session, user: BaseUserCreate):
        user = self.models.User(email=user.email, name=user.name, is_active=user.is_active)
        db.add(user)
        db.commit()
        db.refresh(user)
        return ResponseModel(
            data={"user": user}, message="User created successfully", error=None
        )
