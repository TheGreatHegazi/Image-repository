from typing import Optional, List
from fastapi import FastAPI, File, UploadFile, HTTPException, Header
from PIL import Image
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import re
import os
from pydantic import BaseModel
import base64
from sqlalchemy.orm import Session

from .db import ops, models, schema
from .db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
anon = ops.create_user(SessionLocal(), schema.UserCreate(email="anon@anon.com", username="anonymous", password="password123"))
print (anon)
REGEX_EMAIL = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

app = FastAPI()
APP_ROOT = '/app'
public = os.path.join(APP_ROOT, 'publicimages/')
users = os.path.join(APP_ROOT, 'users/')
os.mkdir(public)
os.mkdir(users)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def read_root():
    return {"Hello": "World"}
@app.get("/try")
def thisworks():
    return {'hello': ops.get_user_by_username(SessionLocal(), "ahmedadel2")}


@app.post("/login")
def login(user: schema.UserLogin):
    if  user.username == None or user.username == '':
        raise HTTPException(status_code=400, detail="username cannot be empty")
    if  user.password == None or user.password == '':
        raise HTTPException(status_code=400, detail="password cannot be empty")
    db_user = ops.get_user_by_username(SessionLocal(), user.username)
    if(not db_user):
        print("not found" )
        raise HTTPException(status_code=400, detail="username and password do not match")
    if user.username == db_user.username and encode(user.password) == "b'"+db_user.password+"'":
        return {'token' : db_user.token}
    else:
        raise HTTPException(status_code=404, detail="Username and password do not match ")


@app.post("/signup")
def create_user(user: schema.UserCreate):
    if  user.username == None or user.username == '':
        raise HTTPException(status_code=400, detail="username cannot be empty")
    
    if  user.password == None or user.password == '':
        raise HTTPException(status_code=400, detail="password cannot be empty")
    if  user.email == None or user.email == '':
        raise HTTPException(status_code=400, detail="email cannot be empty")
    sname = ops.get_user_by_username(SessionLocal(), user.username)
    if(sname):
        raise HTTPException(status_code=400, detail="Username already taken")
    
    db_user = ops.create_user(SessionLocal(), user)
    if(not db_user):
        raise HTTPException(status_code=400, detail="failed to create user")
    target = os.path.join(users, db_user.username +"/")
    os.mkdir(target)
    return {'msg': 'User Created!' }


@app.get("/user/{username}")
def get_user(username: str, token: Optional[str]=Header(None)):

    if isAuth(username, token):
        return {"msg": ops.get_user_by_username(SessionLocal(),username)}
    else:
        raise HTTPException(status_code=401, detail=token) 


@app.get("/images/public")
def get_all_images_paths():
    target = public
    images = os.listdir(target)
    if images.count == 0:
        raise HTTPException(status_code=404, detail="No images saved")
    return {"imgNames": images}

@app.get("/user/{username}/images")
def get_all_images_paths(username, token: Optional[str]=Header(None)):
    if not isAuth(username, token):
        raise HTTPException(status_code=401, detail="UnAuthorized") 
    target = os.path.join(users, username + "/")
    images = os.listdir(target)
    if images.count == 0:
        raise HTTPException(status_code=404, detail="No images saved")

    return {"imgNames": images}

@app.get("/images/{imgname}")
def get_image(imgname):
    target = public
    images = os.listdir(target)
    if images.count == 0:
        raise HTTPException(status_code=404, detail="No images saved")
    if (imgname not in os.listdir(target)):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(os.path.join(target, imgname))

@app.get("/user/{username}/images/{imgname}")
def get_image(username, imgname, token: Optional[str]=Header(None)):

    target = os.path.join(APP_ROOT, 'users/'+ username + '/')
    images = os.listdir(target)
    if images.count == 0:
        raise HTTPException(status_code=404, detail="No images saved")
    if (imgname not in os.listdir(target)):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(os.path.join(target, imgname))



@app.post("/images/public")
async def add_image(image: UploadFile = File(...)):
    target = public
    addImage(target, image)
    ops.create_user_image(SessionLocal(), {name: image.filename, is_public: True}, anon.id)
    return {"response": "successfully added " + image.filename + " Publicly"}

@app.post("/images/public/bulk")
async def add_image(images: List[UploadFile] = File(...)):

    target = public
    for image in images:
        addImage(target, image)
        imgs = ops.create_user_image(SessionLocal(), schema.ImageCreate(name=image.filename, is_public=True), anon.id)
    return {"response": "successfully added all images Publicly"}

@app.post("/user/{username}/images/bulk")
async def add_image(username, images: List[UploadFile] = File(...), token: Optional[str]=Header(None)):
    if not isAuth(username, token):
        raise HTTPException(status_code=401, detail="UnAuthorized") 
    target = os.path.join(APP_ROOT, 'users/'+ username+'/')
    db_user = ops.get_user_by_token(SessionLocal(), token)
    for image in images:
        addImage(target, image)
        imgs = ops.create_user_image(SessionLocal(), schema.ImageCreate(name=image.filename, is_public=False), db_user.id)
    return {"response": "successfully added  all Images Privately"}


@app.post("/user/{username}/images")
async def add_image(username, image: UploadFile = File(...), token: Optional[str]=Header(None)):
    if not isAuth(username, token):
        raise HTTPException(status_code=401, detail="UnAuthorized") 
    target = os.path.join(APP_ROOT, 'users/'+ username+'/')
    addImage(target, image)
    return {"response": "successfully added " + image.filename + " Privately"}
    
def encode(message):
    return str(base64.b64encode(message.encode('ascii')))

def decode(message):
    return str(base64.b64decode(message))

def addImage(target, image):
    
    filename = image.filename

    ext = os.path.splitext(filename)[1]
    if not (ext == ".jpg") and not (ext == ".png") and not (ext == ".bmp"):
        raise HTTPException(status_code=422, detail="File not in a supported format. Please use .jpg, .png, .bmp only")

    destination = "/".join([target, filename])
    try:
        with Image.open(image.file) as im:
            im.save(destination)
    except OSError:
        print("cannot convert", filename)
    return True

def isAuth(username, token):
    if token == '' or token == None or username == None or username == '':
        return False
    
    db_user = ops.get_user_by_token(SessionLocal(), token)
    if (not db_user and db_user.username != username):
        return False
    return True