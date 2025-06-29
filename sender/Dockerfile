FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN pip install poetry==1.6.1
COPY pyproject.toml /app/
RUN poetry install --no-interaction --no-dev

COPY . /app

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
