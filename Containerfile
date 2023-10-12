FROM python:3-alpine

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

RUN adduser -D -H app && chown -R app:app /opt/

COPY --chown=app:app ./src /opt/

USER app

WORKDIR /opt/

CMD [ "python", "/opt/main.py" ]