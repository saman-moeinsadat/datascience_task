FROM python:3.7

COPY app /deploy/app

RUN pip3 install -r /deploy/app/requirements.txt

WORKDIR /deploy
CMD python3 app/app.py
