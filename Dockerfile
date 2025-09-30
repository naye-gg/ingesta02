FROM python:3-slim

WORKDIR /programas/ingesta

# Instalamos dependencias necesarias
RUN pip3 install boto3 pymysql

COPY . .

CMD ["python3", "./ingesta.py"]

