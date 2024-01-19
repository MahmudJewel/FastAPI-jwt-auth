from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from typing import Annotated
from jose import JWTError, jwt

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

# partial update user by id 
@app.patch("/user/{user_id}", response_model=schemas.User)
def update_user_partially(user_id: int, user:schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_db_user = functions.update_user_partially(db=db, user_id=user_id, updated_user=user)
    return updated_db_user

# update user by id 
@app.put("/user/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user:schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_db_user = functions.update_user(db=db, user_id=user_id, updated_user=user)
    return updated_db_user

# delete user by id 
@app.delete("/user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    delete_user = functions.delete_user(db=db, user_id=user_id)
    return delete_user

# getting access token for login 
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
) -> schemas.Token:
    member = functions.authenticate_user(db, user=user)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = functions.create_access_token(
        data={"sub": member.email}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")
