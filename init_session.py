import os
from dotenv import load_dotenv
from pyrogram import Client

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSIONS_DIR = os.path.join(BASE_DIR, 'sessions')
os.makedirs(SESSIONS_DIR, exist_ok=True)

TG_API_ID = int(os.environ['TG_API_ID'])
TG_API_HASH = os.environ['TG_API_HASH']
TG_SESSION_NAME = os.environ['TG_SESSION_NAME']
TG_PHONE_NUMBER = os.getenv('TG_PHONE_NUMBER')

app = Client(
    TG_SESSION_NAME,
    api_id=TG_API_ID,
    api_hash=TG_API_HASH,
    workdir=SESSIONS_DIR,
    phone_number=TG_PHONE_NUMBER,
)

if __name__ == '__main__':
    app.start()
    app.stop()
    print(f'Session initialised at {SESSIONS_DIR}')
