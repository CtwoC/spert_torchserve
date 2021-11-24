# syntax=docker/dockerfile:1

FROM pytorch/torchserve:latest
# FROM python:3.8.12

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html

COPY . .

CMD [ "python3", "server.py"]