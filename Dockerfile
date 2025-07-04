# CF/Backend/Dockerfile
FROM python:3.13-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential python3-dev \
    curl && rm -rf /var/lib/apt/lists/*
RUN ln -sf /usr/local/bin/python3 /usr/local/bin/python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]