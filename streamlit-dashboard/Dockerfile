FROM python:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ .

ENV PYTHONPATH="/app"

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "src/visualization/main.py"]
