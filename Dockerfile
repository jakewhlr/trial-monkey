# set base image (host OS)
FROM python:3.8

WORKDIR /code

COPY requirements.txt .
COPY docs/config.json .

RUN pip install -r requirements.txt

COPY src/ .

CMD [ "python", "main.py", "-c", "./config.json", "-e", "staging" ]