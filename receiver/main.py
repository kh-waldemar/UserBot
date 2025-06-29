import os
import threading
import time
import requests
from flask import Flask, send_from_directory
from pyrogram import Client, filters
from dotenv import load_dotenv

load_dotenv()

MEDIA_DIR = os.path.join(os.getcwd(), "userbot_media")
PUBLIC_MEDIA_HOST = os.getenv("PUBLIC_MEDIA_HOST", "localhost")
PUBLIC_MEDIA_PORT = int(os.getenv("PUBLIC_MEDIA_PORT", 8181))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_API_KEY = os.getenv("WEBHOOK_API_KEY")

app = Flask(__name__)

@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(MEDIA_DIR, filename)


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


def start_flask():
    app.run(host="0.0.0.0", port=PUBLIC_MEDIA_PORT)


if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR, exist_ok=True)

TG_API_ID = int(os.environ['TG_API_ID'])
TG_API_HASH = os.environ['TG_API_HASH']
TG_SESSION_NAME = os.environ['TG_SESSION_NAME']

client = Client(TG_SESSION_NAME, api_id=TG_API_ID, api_hash=TG_API_HASH, workdir="sessions")


@client.on_message(filters.all)
async def handle_message(_, message):
    file_url = None
    if message.media:
        file_path = await message.download(file_name=os.path.join(MEDIA_DIR, f"{message.id}"))
        file_url = f"http://{PUBLIC_MEDIA_HOST}:{PUBLIC_MEDIA_PORT}/media/{os.path.basename(file_path)}"
    data = message.to_dict()
    if file_url:
        data['file_url'] = file_url
    headers = {}
    if WEBHOOK_API_KEY:
        headers['x-api-key'] = WEBHOOK_API_KEY
    if WEBHOOK_URL:
        try:
            requests.post(WEBHOOK_URL, json=data, headers=headers, timeout=5)
        except Exception as e:
            print(f"Failed to send webhook: {e}")


def main():
    threading.Thread(target=start_flask, daemon=True).start()
    threading.Thread(target=cleanup_media, daemon=True).start()
    client.run()


if __name__ == "__main__":
    main()
