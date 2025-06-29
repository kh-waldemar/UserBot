# UserBot

Simple Telegram userbot built with Pyrogram. It receives all messages from your account and can send messages via a REST API. Media files are downloaded and served over HTTP. Webhooks can be used to forward incoming updates.

## Requirements
- Python 3.10+
- Telegram API credentials
- Pip dependencies listed below

## Installation
```bash
# clone the repository and enter it
# make sure Python and pip are available
pip install -r requirements.txt
```

If there is no `requirements.txt`, install dependencies manually:
```bash
pip install pyrogram tgcrypto fastapi uvicorn flask python-dotenv httpx
```

## Configuration
Create a `.env` file in the repository root with the following variables:
```
TG_API_ID=your_api_id
TG_API_HASH=your_api_hash
TG_SESSION_NAME=session
TG_PHONE_NUMBER=+380...   # optional if session already authorised

# Host/port for serving downloaded media
PUBLIC_MEDIA_HOST=your-public-host
PUBLIC_MEDIA_PORT=8181

# Webhook for incoming updates (optional)
WEBHOOK_URL=https://example.com/hook
WEBHOOK_API_KEY=secret

# Token for calling the REST API (optional)
X_API_TOKEN=your_api_token
API_PORT=8001
```

Create necessary folders:
```bash
mkdir -p sessions userbot_media
python init_session.py   # run once to generate the session
```

## Running
```bash
python userbot.py
```

The first run requires logging in with the phone number specified in `TG_PHONE_NUMBER`. Pyrogram will prompt for the code in the console and, if enabled, your two‑factor password. Subsequent runs will reuse the generated session from the `sessions` folder.

## API
- `POST /sendMessage`
- `POST /sendPhoto`
- `POST /sendDocument`
- `POST /sendAudio`
- `POST /sendVoice`
- `POST /sendVideo`
- `POST /sendAnimation`
- `POST /sendVideoNote`
- `POST /sendLocation`
- `POST /sendContact`
- `POST /editMessageText`
- `POST /deleteMessage`

All endpoints expect JSON payloads matching the fields in `userbot.py`. If `X_API_TOKEN` is set, send it via the `x-api-key` header.

Downloaded media is available from `http://<PUBLIC_MEDIA_HOST>:<PUBLIC_MEDIA_PORT>/media/<filename>` and cleaned automatically after three days.

Check the logs in the console to verify the bot has started and is connected. To test webhooks, send a message to your account and ensure the configured URL receives a POST with the update.

