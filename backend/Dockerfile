# Use Python 3.10 slim image as base
FROM python:3.10-slim

# Set environment variables
ENV MODBUS_SERVER_IP=192.168.0.16
ENV MODBUS_SERVER_PORT=5007

# Set working directory
WORKDIR /app

# Copy drift server script into container
COPY drift_server.py /app/drift_server.py

# Install required Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Set default command to run drift_server.py
CMD ["python", "drift_server.py"]
