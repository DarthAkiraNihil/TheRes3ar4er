FROM python:3.10.13-slim-bullseye

COPY requirements.txt requirements.txt
COPY bot.py bot.py
COPY r34API.py r34API.py
COPY logDumper.py logDumper.py
COPY messages.py messages.py
COPY config.py config.py
COPY activityList.py activityList.py

RUN echo Files have been copied
RUN pip install --user -r requirements.txt

CMD ["python", "bot.py"]
