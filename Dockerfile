FROM python:3.10

#RUN apt-get update && apt-get install -y gettext && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

COPY ./src .

CMD wait-for-it -s "${REDIS_HOST}:${REDIS_PORT}" -s "${ELASTIC_HOST}:${ELASTIC_PORT}" --timeout 120 && python main.py