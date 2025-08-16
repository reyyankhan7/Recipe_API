from fastapi import FastAPI
from database import Base, engine
from models import User, Recipe
from auth_router import auth_router
from recipe_router import recipe_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Recipe API")

app.include_router(auth_router)
app.include_router(recipe_router)
