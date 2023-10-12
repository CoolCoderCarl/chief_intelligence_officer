FROM python:3-alpine

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

WORKDIR /opt/

CMD [ "python", "/opt/main.py" ]