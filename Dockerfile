FROM python:3.10-slim-buster

RUN apt update && apt upgrade -y
RUN apt-get install git curl python3-pip ffmpeg -y

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -U -r requirements.txt
COPY . .

CMD python3 -m Chizuru
