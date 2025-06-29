# UserBot

This repository contains a simple Telegram user account service built with **Pyrogram**. It consists of two services:

- **receiver** – receives all updates from Telegram, stores media locally and forwards events to a webhook.
- **sender** – provides a REST API compatible with the Telegram Bot API for sending messages as a user.

Both services are packaged with Docker and share the same Pyrogram session.

## Requirements
- Docker and Docker Compose
- A Telegram account

## Setup

1. Copy `.env.example` to `.env` and fill all variables.
2. Create the directories `sessions/` and `userbot_media/` next to `docker-compose.yml`.
3. Initialize the Pyrogram session:
   ```bash
   python3 init_session.py
   ```
4. Build images and start services:
   ```bash
   docker-compose build
   docker-compose up -d
   ```
5. Check receiver logs:
   ```bash
   docker-compose logs -f receiver
   ```
6. Use the sender API via `http://0.0.0.0:8001`.
7. Media files are available at
   ```
   http://<PUBLIC_MEDIA_HOST>:<PUBLIC_MEDIA_PORT>/media/<filename>
   ```
   Files are automatically removed after three days.

## Files
- `receiver/` – receiver service sources and Dockerfile
- `sender/` – sender service sources and Dockerfile
- `docker-compose.yml` – compose file running both services
- `init_session.py` – interactive script to create a Pyrogram session

Deployment is manual and done only via Docker.
