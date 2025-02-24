FROM python:3.11-buster
LABEL authors='Yan'

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /blog_tg

RUN apt-get update && \
    apt install -y python3-dev

COPY requirenments.txt /blog_backend/requirenments.txt


RUN pip install --upgrade pip
RUN pip install -r /blog_backend/requirenments.txt
COPY . /blog_backend/

COPY . /blog_tg/

ENV PYTHONPATH=/blog_tg/src



CMD  python bot/main.py

EXPOSE 8080