from typing import Optional, List
from fastapi import FastAPI, File, UploadFile, HTTPException, Header
from PIL import Image
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import re
import os
from pydantic import BaseModel
import base64


REGEX_EMAIL = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

class User(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

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
@app.post("/login")
def login(user: UserLogin):
    if  user.username == None or user.username == '':
        raise HTTPException(status_code=400, detail="username cannot be empty")
    if  user.password == None or user.password == '':
        raise HTTPException(status_code=400, detail="password cannot be empty")

    target = os.path.join(APP_ROOT, 'users/'+user.username)
    if(not os.path.isdir(target)):
        raise HTTPException(status_code=400, detail="Username not found")
    
    f = open(target + '.txt', 'r')
    m = f.readline()
    f.close()

    cred = decode(m.split("'")[1]).split("'")[1].split(';')
    username = cred[0].split(',')[0]
    email = cred [0].split(',')[1]
    pwd = cred[1]
    if user.username == username and user.password == pwd:
        return {'token' : encode(username+','+email+';'+pwd) }
    else:
        raise HTTPException(status_code=404, detail="Username and password do not match ")


@app.post("/signup")
def create_user(user: User):
    if  user.username == None or user.username == '':
        raise HTTPException(status_code=400, detail="username cannot be empty")
    
    if  user.password == None or user.password == '':
        raise HTTPException(status_code=400, detail="password cannot be empty")

    target = os.path.join(APP_ROOT, 'users/'+user.username)
    if(os.path.isdir(target)):
        raise HTTPException(status_code=400, detail="Username already Exists")

    os.mkdir(target)
    f = open(target + '.txt', 'w')
    f.write(encode(user.username+','+user.email+';'+user.password))
    f.close()
    return {'msg': 'User Created!'}


@app.get("/user/{username}")
def get_user(username: str, token: Optional[str]=Header(None)):

    if isAuth(username, token):
        return {"msg": decode(token.split("'")[1]).split("'")[1].split(';')[0]}
    else:
        raise HTTPException(status_code=401, detail="UnAuthorized") 


@app.get("/images/public")
def get_all_images_paths():
    target = os.path.join(APP_ROOT, 'publicimages/')
    images = os.listdir(target)
    if images.count == 0:
        raise HTTPException(status_code=404, detail="No images saved")
    return {"imgNames": images}

@app.get("/user/{username}/images")
def get_all_images_paths(username, token: Optional[str]=Header(None)):
    if not isAuth(username, token):
        raise HTTPException(status_code=401, detail="UnAuthorized") 

    target = os.path.join(APP_ROOT, 'users/' + username)
    
    images = os.listdir(target)
    if images.count == 0:
        raise HTTPException(status_code=404, detail="No images saved")

    return {"imgNames": images}

@app.get("/images/{imgname}")
def get_image(imgname):
    target = os.path.join(APP_ROOT, 'publicimages/')
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
    target = os.path.join(APP_ROOT, 'publicimages/')
    addImage(target, image)
    return {"response": "successfully added " + image.filename + " Publicly"}

@app.post("/images/public/bulk")
async def add_image(images: List[UploadFile] = File(...)):
    target = os.path.join(APP_ROOT, 'publicimages/')
    for image in images:
        addImage(target, image)
    return {"response": "successfully added all images Publicly"}

@app.post("/user/{username}/images/bulk")
async def add_image(username, images: List[UploadFile] = File(...), token: Optional[str]=Header(None)):
    if not isAuth(username, token):
        raise HTTPException(status_code=401, detail="UnAuthorized") 
    target = os.path.join(APP_ROOT, 'users/'+ username+'/')
    for image in images:
        addImage(target, image)
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
    target = os.path.join(APP_ROOT, 'users/' + username)
    f = open(target + '.txt', 'r')
    m = f.readline()
    f.close()
    if token != m :
        return False
    return True