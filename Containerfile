FROM python:3-alpine

RUN adduser app && chown -R app:app /opt/

COPY --chown=app:app ./src /opt/

USER app

CMD [ "python", "/opt/main.py" ]