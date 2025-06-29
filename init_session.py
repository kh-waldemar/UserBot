import os
from pyrogram import Client
from dotenv import load_dotenv

load_dotenv()

TG_API_ID = int(os.environ['TG_API_ID'])
TG_API_HASH = os.environ['TG_API_HASH']
TG_SESSION_NAME = os.environ['TG_SESSION_NAME']
TG_PHONE_NUMBER = os.environ.get('TG_PHONE_NUMBER')

if not os.path.exists('sessions'):
    os.makedirs('sessions')

app = Client(TG_SESSION_NAME, api_id=TG_API_ID, api_hash=TG_API_HASH, workdir="sessions", phone_number=TG_PHONE_NUMBER)

app.start()
print("Session initialized and saved.")
app.stop()
