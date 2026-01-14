FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY mock_server.py .
COPY mock_data/ ./mock_data/

EXPOSE 8080

CMD ["python", "mock_server.py"]