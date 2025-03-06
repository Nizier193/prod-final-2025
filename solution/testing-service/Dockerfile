FROM python:latest

WORKDIR /app

COPY requirements.txt .

# Явная установка pytest и вывод установленных пакетов для проверки
RUN pip install pytest pytest && \
    pip install -r requirements.txt && \
    pip list

COPY . .

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENV PYTHONPATH="/app"

ENTRYPOINT ["./entrypoint.sh"]
CMD ["all"]  # значение по умолчанию
