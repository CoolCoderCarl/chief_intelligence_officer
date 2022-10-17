FROM python:3-alpine

COPY main.py /

CMD [ "python", "./main.py" ]