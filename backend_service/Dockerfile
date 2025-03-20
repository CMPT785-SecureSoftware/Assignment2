FROM python:alpine3.16

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY utils/ utils/
COPY app.py app.py

CMD ["python", "app.py"]