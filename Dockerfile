FROM python:3.9

COPY main.py.py /

ENTRYPOINT [ "python" ]

CMD [ "./main.py" ]