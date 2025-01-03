# Base image for Django
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Expose the application port
EXPOSE 10000

# Default command
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:10000"]
