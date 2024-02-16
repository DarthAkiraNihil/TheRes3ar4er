FROM python:3.10.13-slim-bullseye

COPY requirements.txt requirements.txt

COPY main.py main.py

COPY rule34api.py rule34api.py

COPY config.py config.py

RUN pip install --user -r requirements.txt

CMD ["python", "main.py"]
