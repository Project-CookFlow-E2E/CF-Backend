# # CF-backend/Dockerfile
# FROM python:3.13-slim
# WORKDIR /app
# RUN apt-get update && apt-get install -y curl --no-install-recommends && rm -rf /var/lib/apt/lists/*
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# COPY . .

# CF-backend/Dockerfile
FROM python:3.13-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl --no-install-recommends && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# --- ADD THIS LINE ---
# Command to run the Django development server
# Make sure your Django project's manage.py is at the root of /app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]