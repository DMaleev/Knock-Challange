from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, status, WebSocket, Cookie, Query, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware

from pydantic import ValidationError
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

import json

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://192.168.1.6:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/thread/", response_model=schemas.Thread)
def create_thread(thread: schemas.ThreadCreate, db: Session = Depends(get_db)):
    try:
        if(len(thread.users) < 2):
            raise HTTPException(status_code=200, detail="Thread can only be created for 2 or more users")
        db_thread = crud.create_thread(db, thread=thread)
        return db_thread
    except ValidationError as e:
        return HTTPException(status_code=200, detail=str(e))

@app.post("/thread/{thread_id}/{username}", status_code=203)
def send_message(thread_id: int, username: str, message:schemas.MessageBase, db: Session = Depends(get_db)):
    thread = crud.get_thread(db=db, thread_id=thread_id)
    if not thread:
        raise HTTPException(status_code=200, detail="Thread with given id not found")
    user = crud.get_user_by_username(db=db, username=username)
    if not user:
        raise HTTPException(status_code=200, detail="User with given username not found")
    if not crud.check_permission(db=db, thread=thread, user=user):
        raise HTTPException(status_code=403, detail="User does't have a permission to write in this thread")
    try:
        message = schemas.MessageCreate(message=message.message, thread=thread, user=user)
        crud.send_message(db=db, message=message)
    except ValidationError as e:
        return HTTPException(status_code=200, detail=str(e))

@app.get("/thread/{thread_id}", response_model=schemas.Messages)
def get_thread(thread_id: int, db: Session = Depends(get_db)):
    thread = crud.get_thread(db=db, thread_id=thread_id)
    if not thread:
        raise HTTPException(status_code=200, detail="Thread with given id not found")
    messages = crud.get_messages(db=db, thread=thread)
    return {'messages': messages}
    
    
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, username: str):
        for connection in self.active_connections:
            await connection.send_text({"message":message, "username": username})


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            await manager.broadcast(json.loads(data)["message"], json.loads(data)["username"])
    except WebSocketDisconnect:
        manager.disconnect(websocket)
