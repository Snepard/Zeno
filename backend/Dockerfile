FROM python:3.10-slim

WORKDIR /app

# Install system dependencies required for building psycopg2 and other packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Setting pythonpath mapped to the working directory
ENV PYTHONPATH=/app
