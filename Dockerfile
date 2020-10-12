# set base image (host OS)
FROM python:3.8

WORKDIR /code

COPY requirements.txt .
COPY config.json .

RUN pip install -r requirements.txt

COPY src/ .

ENTRYPOINT ["python", "main.py"]
CMD ["-c", "./config.json", "-e", "staging"]