import os
import threading
import time
import asyncio
import requests
from dotenv import load_dotenv
from pyrogram import Client, filters, idle
from flask import Flask, send_from_directory
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import uvicorn

load_dotenv()

# Directories
if not os.path.exists('sessions'):
    os.makedirs('sessions', exist_ok=True)

MEDIA_DIR = os.path.join(os.getcwd(), 'userbot_media')
if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR, exist_ok=True)

# Environment
TG_API_ID = int(os.environ['TG_API_ID'])
TG_API_HASH = os.environ['TG_API_HASH']
TG_SESSION_NAME = os.environ['TG_SESSION_NAME']
TG_PHONE_NUMBER = os.getenv('TG_PHONE_NUMBER')

PUBLIC_MEDIA_HOST = os.getenv('PUBLIC_MEDIA_HOST', 'localhost')
PUBLIC_MEDIA_PORT = int(os.getenv('PUBLIC_MEDIA_PORT', 8181))
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
WEBHOOK_API_KEY = os.getenv('WEBHOOK_API_KEY')
X_API_TOKEN = os.getenv('X_API_TOKEN')
API_PORT = int(os.getenv('API_PORT', 8001))

# Flask app for media
flask_app = Flask(__name__)

@flask_app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(MEDIA_DIR, filename)

# FastAPI app for sending messages
api_app = FastAPI()

client = Client(TG_SESSION_NAME, api_id=TG_API_ID, api_hash=TG_API_HASH, workdir='sessions', phone_number=TG_PHONE_NUMBER)

# Helper to verify API key
def verify_key(key: str | None):
    if X_API_TOKEN and key != X_API_TOKEN:
        raise HTTPException(status_code=401, detail='Invalid API key')

# Webhook sender
def post_webhook(data: dict):
    if not WEBHOOK_URL:
        return
    headers = {}
    if WEBHOOK_API_KEY:
        headers['x-api-key'] = WEBHOOK_API_KEY
    try:
        requests.post(WEBHOOK_URL, json=data, headers=headers, timeout=5)
    except Exception as e:
        print(f'Failed to send webhook: {e}')

# Cleanup task for media
def cleanup_media():
    while True:
        now = time.time()
        for f in os.listdir(MEDIA_DIR):
            fp = os.path.join(MEDIA_DIR, f)
            if os.path.isfile(fp) and now - os.path.getmtime(fp) > 3 * 24 * 3600:
                try:
                    os.remove(fp)
                except Exception:
                    pass
        time.sleep(3600)

# Receiver handlers
@client.on_message(filters.all)
async def handle_message(_, message):
    file_url = None
    if message.media:
        file_path = await message.download(file_name=os.path.join(MEDIA_DIR, f"{message.id}"))
        file_url = f"http://{PUBLIC_MEDIA_HOST}:{PUBLIC_MEDIA_PORT}/media/{os.path.basename(file_path)}"
    data = message.to_dict()
    if file_url:
        data['file_url'] = file_url
    post_webhook(data)

@client.on_edited_message(filters.all)
async def handle_edited(_, message):
    data = message.to_dict()
    data['edited'] = True
    post_webhook(data)

@client.on_inline_query()
async def handle_inline(_, inline_query):
    data = inline_query.to_dict()
    post_webhook(data)

# API models and endpoints
class SendMessage(BaseModel):
    chat_id: int | str
    text: str

class SendPhoto(BaseModel):
    chat_id: int | str
    photo: str
    caption: str | None = None

class SendDocument(BaseModel):
    chat_id: int | str
    document: str
    caption: str | None = None

class SendAudio(BaseModel):
    chat_id: int | str
    audio: str
    caption: str | None = None

class SendVoice(BaseModel):
    chat_id: int | str
    voice: str
    caption: str | None = None

class SendVideo(BaseModel):
    chat_id: int | str
    video: str
    caption: str | None = None

class SendAnimation(BaseModel):
    chat_id: int | str
    animation: str
    caption: str | None = None

class SendVideoNote(BaseModel):
    chat_id: int | str
    video_note: str

class SendLocation(BaseModel):
    chat_id: int | str
    latitude: float
    longitude: float

class SendContact(BaseModel):
    chat_id: int | str
    phone_number: str
    first_name: str
    last_name: str | None = None

class EditMessageText(BaseModel):
    chat_id: int | str
    message_id: int
    text: str

class DeleteMessage(BaseModel):
    chat_id: int | str
    message_id: int

@api_app.on_event('startup')
async def startup():
    await client.start()

@api_app.on_event('shutdown')
async def shutdown():
    await client.stop()

@api_app.post('/sendMessage')
async def send_message(data: SendMessage, x_api_key: str | None = Header(default=None)):
    verify_key(x_api_key)
    msg = await client.send_message(chat_id=data.chat_id, text=data.text)
    return {'message_id': msg.id}

@api_app.post('/sendPhoto')
async def send_photo(data: SendPhoto, x_api_key: str | None = Header(default=None)):
    verify_key(x_api_key)
    msg = await client.send_photo(chat_id=data.chat_id, photo=data.photo, caption=data.caption)
    return {'message_id': msg.id}

@api_app.post('/sendDocument')
async def send_document(data: SendDocument, x_api_key: str | None = Header(default=None)):
    verify_key(x_api_key)
    msg = await client.send_document(chat_id=data.chat_id, document=data.document, caption=data.caption)
    return {'message_id': msg.id}

@api_app.post('/sendAudio')
async def send_audio(data: SendAudio, x_api_key: str | None = Header(default=None)):
    verify_key(x_api_key)
    msg = await client.send_audio(chat_id=data.chat_id, audio=data.audio, caption=data.caption)
    return {'message_id': msg.id}

@api_app.post('/sendVoice')
async def send_voice(data: SendVoice, x_api_key: str | None = Header(default=None)):
    verify_key(x_api_key)
    msg = await client.send_voice(chat_id=data.chat_id, voice=data.voice, caption=data.caption)
    return {'message_id': msg.id}

@api_app.post('/sendVideo')
async def send_video(data: SendVideo, x_api_key: str | None = Header(default=None)):
    verify_key(x_api_key)
    msg = await client.send_video(chat_id=data.chat_id, video=data.video, caption=data.caption)
    return {'message_id': msg.id}

@api_app.post('/sendAnimation')
async def send_animation(data: SendAnimation, x_api_key: str | None = Header(default=None)):
    verify_key(x_api_key)
    msg = await client.send_animation(chat_id=data.chat_id, animation=data.animation, caption=data.caption)
    return {'message_id': msg.id}

@api_app.post('/sendVideoNote')
async def send_video_note(data: SendVideoNote, x_api_key: str | None = Header(default=None)):
    verify_key(x_api_key)
    msg = await client.send_video_note(chat_id=data.chat_id, video_note=data.video_note)
    return {'message_id': msg.id}

@api_app.post('/sendLocation')
async def send_location(data: SendLocation, x_api_key: str | None = Header(default=None)):
    verify_key(x_api_key)
    msg = await client.send_location(chat_id=data.chat_id, latitude=data.latitude, longitude=data.longitude)
    return {'message_id': msg.id}

@api_app.post('/sendContact')
async def send_contact(data: SendContact, x_api_key: str | None = Header(default=None)):
    verify_key(x_api_key)
    msg = await client.send_contact(chat_id=data.chat_id, phone_number=data.phone_number, first_name=data.first_name, last_name=data.last_name)
    return {'message_id': msg.id}

@api_app.post('/editMessageText')
async def edit_message_text(data: EditMessageText, x_api_key: str | None = Header(default=None)):
    verify_key(x_api_key)
    msg = await client.edit_message_text(chat_id=data.chat_id, message_id=data.message_id, text=data.text)
    return {'message_id': msg.id}

@api_app.post('/deleteMessage')
async def delete_message(data: DeleteMessage, x_api_key: str | None = Header(default=None)):
    verify_key(x_api_key)
    await client.delete_messages(chat_id=data.chat_id, message_ids=data.message_id)
    return {'ok': True}

# Run all services
async def main():
    flask_thread = threading.Thread(target=flask_app.run, kwargs={'host': '0.0.0.0', 'port': PUBLIC_MEDIA_PORT, 'use_reloader': False}, daemon=True)
    flask_thread.start()
    cleanup_thread = threading.Thread(target=cleanup_media, daemon=True)
    cleanup_thread.start()
    config = uvicorn.Config(api_app, host='0.0.0.0', port=API_PORT, log_level='info')
    server = uvicorn.Server(config)
    await asyncio.gather(server.serve(), idle())

if __name__ == '__main__':
    asyncio.run(main())
