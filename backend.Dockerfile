FROM python:3.12-alpine

LABEL maintainer="xyz@ie.com"
LABEL version="1.0"
LABEL description="Python 3.12 Alpine"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk update && \
    apk add --no-cache \
        bash \
        postgresql-client \
        ffmpeg \
        gcc \
        musl-dev \
        postgresql-dev

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN apk del gcc musl-dev postgresql-dev

COPY . .

RUN chmod +x backend.entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./backend.entrypoint.sh"]