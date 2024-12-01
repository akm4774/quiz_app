# Base image for Django
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for Django and PostgreSQL
RUN apt-get update && apt-get install -y \
    pkg-config \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Add wait-for-it script to the image
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Copy the project files
COPY . .

# Copy the .env file to the container
COPY .env .env 

# Expose the application port
EXPOSE 10000

# Default command
CMD ["/start.sh"]
