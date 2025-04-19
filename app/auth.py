from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import schemas, models, utils, database

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = utils.hash_password(user.password)
    new_user = models.User(
        email=user.email,
        hashed_password=hashed_pw,
        full_name=user.full_name
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "email": new_user.email,
        "full_name": new_user.full_name,
        "ok": True
    }

def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not utils.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = utils.create_access_token({"sub": db_user.email})
    return {"ok":True, "full_name": db_user.full_name,"access_token": token, "token_type": "bearer"} 
