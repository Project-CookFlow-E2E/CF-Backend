# # cf-backend/Dockerfile
FROM python:3.13-slim
WORKDIR /app

# Install essential tools and dependencies
RUN apt-get update && \
    apt-get install -y curl postgresql-client --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Set Python to unbuffered mode
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Use direct python execution with unbuffered flag
CMD ["python", "-u", "manage.py", "runserver", "0.0.0.0:8000"]