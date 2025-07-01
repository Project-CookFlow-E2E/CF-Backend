FROM python:3.13-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Set Python unbuffered and ensure pip is up to date
ENV PYTHONUNBUFFERED=1
RUN python -m pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["python", "-u", "manage.py", "runserver", "0.0.0.0:8000"]python", "-u", "manage.py", "runserver", "0.0.0.0:8000"]