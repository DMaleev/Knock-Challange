from datetime import datetime

from typing import List, Optional, Set

from pydantic import BaseModel, validator, Field, constr


class UserBase(BaseModel):
    username: str

    class Config:
        orm_mode = True

class User(UserBase):
    user_id: int

    class Config:
        orm_mode = True

class Thread(BaseModel):
    thread_id: int

    class Config:
        orm_mode = True

class ThreadCreate(BaseModel):
    users: Set[str]

    @validator('users')
    def username_len(cls, v):
        for username in v:
            assert len(username) < 15 and len(username) > 1, 'Username should be between 1-15 characters '
        return v

class Permission(BaseModel):
    user_id: int
    thread_id: int

class PermissionBase(Permission):
    id: int

class MessageBase(BaseModel):
    message: str

    @validator('message')
    def text_too_big(cls, v):
        assert len(v) < 200 and len(v) > 1, 'Message should be be between 1-200 characters'
        return v

class MessageCreate(MessageBase):
    thread: Thread
    user: User

class Message(BaseModel):
    message: str
    username: UserBase = None
    
    @validator('username')
    def extract_username(cls, v):
        return v.username

    class Config:
        orm_mode = True


class Messages(BaseModel):
    messages: List[Message]

    class Config:
        orm_mode = True
