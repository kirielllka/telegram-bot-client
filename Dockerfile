FROM python:3.11-buster
LABEL authors='Yan'

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /blog_tg

RUN apt-get update && \
    apt install -y python3-dev

RUN pip install --upgrade pip
RUN pip install poetry  
COPY pyproject.toml .
RUN apt-get update && \
    apt install -y python3-dev

COPY . /blog_tg/src

ENV PYTHONPATH=/blog_tg/src

WORKDIR /blog_tg/src

CMD ["python", "main.py"]    

EXPOSE 8000