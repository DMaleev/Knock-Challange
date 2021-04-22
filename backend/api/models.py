import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)

class Thread(Base):
    __tablename__ = "threads"

    thread_id = Column(Integer, primary_key=True, index=True)

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    thread_id = Column(Integer, ForeignKey('threads.thread_id'))

class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True, index=True)
    message = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    thread_id = Column(Integer, ForeignKey('threads.thread_id'))

    username = relationship("User")
    thread = relationship("Thread")