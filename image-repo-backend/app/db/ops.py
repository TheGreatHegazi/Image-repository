from sqlalchemy.orm import Session

from . import models, schema
import base64



def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_token(db: Session, token: str):
    return db.query(models.User).filter(models.User.token == token).first()

def create_user(db: Session, user: schema.UserCreate):
    exist = get_user_by_username(db,user.username)
    if(exist):
        return exist
    hashed_password =  base64.b64encode(user.password.encode('ascii'))
    temp = user.email+ ','+ user.username
    token = base64.b64encode((temp).encode('ascii'))
    db_user = models.User(email=user.email, password=hashed_password, username=user.username, token=token, images=[])
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_images(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Images).offset(skip).limit(limit).all()


def get_images_by_owner(db: Session, owner: int):
    return db.query(models.Images).filter(models.Images.owner_id == owner)

def get_image_by_owner_name (db: Session, owner: int, name: str):
    return list(filter(lambda i : i.owner_id == owner, db.query(models.Images).filter(models.Images.name == name)))


def create_user_image(db: Session, image: schema.ImageCreate, user_id: int):
    existing = get_image_by_owner_name(db, user_id, image.name)
    print(existing)
    if(len(existing) > 0):
        return existing[0]
    db_image = models.Images(**image.dict(), owner_id=user_id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image