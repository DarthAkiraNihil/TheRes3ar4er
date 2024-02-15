FROM python

WORKDIR /test

COPY requirements.txt requirements.txt

RUN pip install --user -r requirements.txt

COPY . .

CMD ["python", "main.py"]
