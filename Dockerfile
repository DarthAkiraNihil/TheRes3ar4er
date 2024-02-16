FROM alpine

RUN apt install python

COPY requirements.txt requirements.txt

COPY main.py main.py

COPY rule34api.py rule34api.py

RUN pip install --user -r requirements.txt

CMD ["python", "main.py"]
