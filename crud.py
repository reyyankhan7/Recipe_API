from sqlalchemy.orm import Session
from models import User, Recipe
from schemas import UserCreate, RecipeCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_recipe(db: Session, recipe: RecipeCreate, user_id: int):
    db_recipe = Recipe(title=recipe.title, ingredients=recipe.ingredients, steps=recipe.steps, owner_id=user_id)
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe
    
def get_recipes(db: Session, user_id: int):
    return db.query(Recipe).filter(Recipe.owner_id == user_id).all()

def search_recipes(db: Session, ingredient: str):
    return db.query(Recipe).filter(Recipe.ingredients.contains(ingredient)).all()

def delete_recipe(db: Session, recipe_id: int, user_id: int):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id, Recipe.owner_id == user_id).first()
    if recipe:
        db.delete(recipe)
        db.commit()
        return True
    return False
