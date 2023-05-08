FROM python:3.10

ENV PYTHONPATH=/

WORKDIR /tests

COPY functional/requirements.txt functional/requirements.txt

RUN pip install --upgrade pip

COPY . .
