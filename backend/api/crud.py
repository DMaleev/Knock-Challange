from sqlalchemy.orm import Session
from typing import Set

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_thread(db: Session, thread_id: int):
    return db.query(models.Thread).filter(models.Thread.thread_id == thread_id).first()

def create_user(db: Session, user: schemas.UserBase):
    db_user = get_user_by_username(db=db, username=user.username)
    if not db_user:
        db_user = models.User(username=user.username)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user

def add_permissions(db: Session, thread: models.Thread, users: Set[models.User]):
    try:
        for user in users:
            db_permission = models.Permission(user_id=user.user_id, thread_id=thread.thread_id)
            db.add(db_permission)
            db.commit()
    except:
        return False
    return True

def check_permission(db: Session, user: models.User, thread: models.Thread):
    return db.query(models.Permission).filter(models.Permission.user_id == user.user_id, models.Permission.thread_id == thread.thread_id).first()

def create_thread(db: Session, thread: schemas.ThreadCreate):
    thread_users = [create_user(db=db, user=schemas.UserBase(username=user)) for user in thread.users]
    new_thread = models.Thread()
    db.add(new_thread)
    db.commit()
    db.refresh(new_thread)
    add_permissions(db=db, thread=new_thread, users=thread_users)
    return new_thread

def send_message(db: Session, message: schemas.Message):
    try:
        print(message)
        new_message = models.Message(message=message.message, user_id=message.user.user_id, thread_id=message.thread.thread_id)
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
    except Exception as e:
        return False
    return new_message

def get_messages(db: Session, thread: models.Thread):
    return db.query(models.Message).filter(models.Message.thread_id == thread.thread_id).all()