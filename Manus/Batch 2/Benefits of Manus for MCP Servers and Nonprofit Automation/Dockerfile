FROM python:3.12-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

ENV APP_VERSION=1.0.0 # Default version, can be overridden at build/runtime

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


