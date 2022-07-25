FROM python:3.8

WORKDIR /rp-gui

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./app

CMD ["python", "./app/gui.py"]
