FROM balenalib/raspberrypi3-debian:latest

COPY ./__init__.py ./sensors-pack ./humidity.py ./humidity_config.json ./requirements.txt /

ENV PYTHONUNBUFFERED "1"
ENV PYTHONIOENCODING "UTF-8"

RUN apt-get update -y && \
    apt-get install curl telnet net-tools wget python3 python3-pip -y && \
    pip3 install -r /requirements.txt

CMD [ "python3", "/humidity.py" ]
