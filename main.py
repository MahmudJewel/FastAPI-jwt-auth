from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

# from . import crud, models, schemas
import functions, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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

@app.post("/user/", response_model = schemas.User)
def create_user( user: schemas.UserCreate , db: Session = Depends(get_db)):
    db_user = functions.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return functions.create_user(db=db, user=user)

@app.get("/users/", response_model = list[schemas.User])
def get_all_users( skip:int=0, limit:int=0, db: Session = Depends(get_db)):
    users = functions.get_users(db=db, skip=skip, limit=limit)
    return users


