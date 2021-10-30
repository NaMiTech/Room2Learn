FROM python:latest

RUN apt update
RUN apt install gcc
RUN pip install --upgrade pip


ENV TZ=Europe/Madrid

ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD python entrypoint.py
