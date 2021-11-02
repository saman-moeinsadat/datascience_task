FROM python:3.7

# COPY app /deploy/app
RUN apt-get -y update        
RUN apt-get -y install git
RUN git clone https://github.com/saman-moeinsadat/datascience_task

RUN pip3 install -r /deploy/app/requirements.txt
RUN ./setup.sh

WORKDIR /deploy
CMD python3 app/app.py
