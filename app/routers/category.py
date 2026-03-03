from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from app.database import SessionDep
from app.models import *
from app.auth import encrypt_password, verify_password, create_access_token, AuthDep
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import status

category_router = APIRouter(tags=["Category"])

@category_router.post('/categories', response_model=CategoryResponse)
def create_category(db:SessionDep, user:AuthDep, category_data:CategoryCreate):
    category = Category(text=category_data.text, user_id=user.id)
    try:
        db.add(category)
        db.commit()
        db.refresh(category)
        return category
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="An error occurred while creating an item",
        )
    
@category_router.get('/categories/{cat_id}/todos', response_model=list[CategoryResponse])
def get_todos_by_category(cat_id:int, db:SessionDep, user:AuthDep):
    category = db.exec(select(Category).where(Category.id==cat_id, Category.user_id==user.id)).one_or_none()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    return category.todos