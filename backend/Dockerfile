FROM python:latest

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8080

CMD [ "python", "app/main.py" ]