FROM python:latest

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./app .

ENV PYTHONPATH=/app
ENTRYPOINT ["python", "src/bot/main.py"]
