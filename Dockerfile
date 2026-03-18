FROM python:3.13-slim
LABEL maintainer="Danil Ivanov"

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY bot/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot/ .

HEALTHCHECK --interval=30s --timeout=3s CMD true

CMD ["python", "main.py"]
