from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import RecipeCreate, RecipeOut
from crud import create_recipe, get_recipes, search_recipes, delete_recipe
from auth_router import get_current_user
from typing import List
from fastapi.security import HTTPBearer

security = HTTPBearer()
recipe_router = APIRouter(prefix="/recipes", tags=["recipes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@recipe_router.post("/", response_model=RecipeOut)
def add_recipe(recipe: RecipeCreate, db: Session = Depends(get_db), token: str = Depends(security)):
    user = get_current_user(token.credentials, db)
    return create_recipe(db, recipe, user.id)

@recipe_router.get("/", response_model=List[RecipeOut])
def list_recipes(
    db: Session = Depends(get_db),
    token: str = Depends(security)
):
    user = get_current_user(token.credentials, db)
    return get_recipes(db, user.id)  

@recipe_router.get("/search", response_model=List[RecipeOut])
def search(ingredient: str, db: Session = Depends(get_db)):
    return search_recipes(db, ingredient)

@recipe_router.delete("/{recipe_id}")
def remove_recipe(recipe_id: int, db: Session = Depends(get_db), token: str = Depends(security)):
    user = get_current_user(token.credentials, db)
    success = delete_recipe(db, recipe_id, user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Recipe not found or not owned by user")
    return {"message": "Recipe deleted"}    