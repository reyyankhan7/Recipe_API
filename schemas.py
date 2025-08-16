from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class RecipeBase(BaseModel):
    title: str
    ingredients: str
    steps: str

class RecipeCreate(RecipeBase):
    pass

class RecipeOut(RecipeBase):
    id: int
    owner_id: int
    class Config:
        orm_mode = True
