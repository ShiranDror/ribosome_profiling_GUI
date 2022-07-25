FROM python:3.8

ADD . /app
WORKDIR /rp-gui

COPY requirements.txt .
COPY ./app ./app

RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt

CMD . venv/bin/activate && exec python ./app/gui.py
