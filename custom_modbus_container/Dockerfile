FROM python:3.10-slim

RUN pip install modbus-tk

COPY modbus-server.py /app/modbus-server.py

WORKDIR /app

CMD ["python", "modbus-server.py"]

