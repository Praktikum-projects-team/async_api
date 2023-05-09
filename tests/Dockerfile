FROM python:3.10

ENV PYTHONPATH=/

WORKDIR /tests

COPY functional/requirements.txt functional/requirements.txt

RUN pip install --upgrade pip && pip install -r /tests/functional/requirements.txt

COPY . .

CMD python3 /tests/functional/utils/wait_for_es.py && python3 /tests/functional/utils/wait_for_redis.py && pytest /tests/functional/src

