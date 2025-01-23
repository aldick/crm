FROM python:3.12-alpine

RUN apk update && \
	apk add nano

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /django

COPY ./requirements.txt /django
RUN pip install --no-cache-dir -r requirements.txt

COPY . /django

EXPOSE 8001