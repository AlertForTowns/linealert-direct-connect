# Use a Python base image
FROM python:3.10-slim

# Set environment variable to avoid writing .pyc files
ENV PYTHONUNBUFFERED=1

# Install system dependencies for networking, logging, and troubleshooting
RUN apt-get update && \
    apt-get install -y \
    iputils-ping \
    net-tools \
    curl \
    procps \
    libpq-dev \
    git \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt into the container and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy necessary files into the container
COPY modbus_server.py /app/modbus_server.py
COPY train_stack.py /app/train_stack.py
COPY modbus_server.json /app/modbus_server.json
COPY drift_server.py /app/drift_server.py

# Expose the ports required by the Modbus server (TCP 5020) and Flask (5007)
EXPOSE 5020
EXPOSE 5007

# Start the modbus server with Flask in a background thread
CMD ["python3", "modbus_server.py"]
