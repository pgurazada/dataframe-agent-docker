FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "2", "app:dataframe_agent_api"]