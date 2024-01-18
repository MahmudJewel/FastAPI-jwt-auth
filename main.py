from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session

import functions, models, schemas
from database import SessionLocal, engine
from jwt import users

models.Base.metadata.create_all(bind=engine)

SECRET_KEY = "6a1c3d7dbc5cc0ca18c734f2c39af71644149038bb1292de658060d3422c7028"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()
app.include_router(users.router)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def initialize():
    return {"msg": "Initialization"}

# create new user 
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = functions.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return functions.create_user(db=db, user=user)

# get all users 
@app.get("/users/", response_model=list[schemas.User]) # with Pydantic response model
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = functions.get_users(db, skip=skip, limit=limit)
    return users

# get user by id 
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = functions.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
