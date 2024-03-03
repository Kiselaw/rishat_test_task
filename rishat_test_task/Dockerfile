FROM python:3.11-slim

RUN mkdir /app

COPY requirements.txt /app

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY . /app

WORKDIR /app

COPY ./entrypoint.sh /app

ENTRYPOINT ["sh", "/app/entrypoint.sh" ]
