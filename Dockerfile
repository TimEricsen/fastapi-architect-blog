FROM python:3.8

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt
COPY . /src/