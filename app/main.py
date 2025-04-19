from fastapi import FastAPI, Depends
from . import schemas, auth, models
from .database import engine
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
import os

load_dotenv()

frontend_url = os.getenv("FRONTEND_URL")

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables at startup
@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=engine)

@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db=Depends(auth.get_db)):
    return auth.register_user(user, db)

@app.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db=Depends(auth.get_db)):
    return auth.login_user(user, db)
