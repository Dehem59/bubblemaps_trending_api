FROM python:3.12-slim

WORKDIR /app

COPY setup.py .
COPY src/ ./src/

RUN pip install --no-cache-dir .

# Expose port for Cloud Run
ENV PORT=8080
EXPOSE 8080

CMD ["sh", "-c", "uvicorn infra.app:app --host 0.0.0.0 --port $PORT"]