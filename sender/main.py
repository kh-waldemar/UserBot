import os
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from pyrogram import Client

load_dotenv()

app = FastAPI()

X_API_TOKEN = os.getenv("X_API_TOKEN")
TG_API_ID = int(os.environ['TG_API_ID'])
TG_API_HASH = os.environ['TG_API_HASH']
TG_SESSION_NAME = os.environ['TG_SESSION_NAME']

client = Client(TG_SESSION_NAME, api_id=TG_API_ID, api_hash=TG_API_HASH, workdir="sessions")


@app.on_event("startup")
async def startup():
    await client.start()


@app.on_event("shutdown")
async def shutdown():
    await client.stop()


def verify_key(key: str | None):
    if X_API_TOKEN and key != X_API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API key")


class SendMessage(BaseModel):
    chat_id: int | str
    text: str


@app.post("/sendMessage")
async def send_message(data: SendMessage, x_api_key: str | None = Header(default=None)):
    verify_key(x_api_key)
    msg = await client.send_message(chat_id=data.chat_id, text=data.text)
    return {"message_id": msg.id}


class SendPhoto(BaseModel):
    chat_id: int | str
    photo: str
    caption: str | None = None


@app.post("/sendPhoto")
async def send_photo(data: SendPhoto, x_api_key: str | None = Header(default=None)):
    verify_key(x_api_key)
    msg = await client.send_photo(chat_id=data.chat_id, photo=data.photo, caption=data.caption)
    return {"message_id": msg.id}


class EditMessageText(BaseModel):
    chat_id: int | str
    message_id: int
    text: str


@app.post("/editMessageText")
async def edit_message_text(data: EditMessageText, x_api_key: str | None = Header(default=None)):
    verify_key(x_api_key)
    msg = await client.edit_message_text(chat_id=data.chat_id, message_id=data.message_id, text=data.text)
    return {"message_id": msg.id}


class DeleteMessage(BaseModel):
    chat_id: int | str
    message_id: int


@app.post("/deleteMessage")
async def delete_message(data: DeleteMessage, x_api_key: str | None = Header(default=None)):
    verify_key(x_api_key)
    await client.delete_messages(chat_id=data.chat_id, message_ids=data.message_id)
    return {"ok": True}
