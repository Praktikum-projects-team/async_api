FROM python:3.10

WORKDIR /tests

COPY /functional/requirements.txt /functional/requirements.txt

RUN  pip install --upgrade pip
#     && pip install -r /functional/requirements.txt

COPY . .

#RUN python -m venv /venv
#ENV PATH="/venv/bin:$PATH"
#
#COPY . /tests/
#
#RUN /venv/bin/pip install --upgrade pip
#RUN /venv/bin/pip install -r /tests/functional/requirements.txt
