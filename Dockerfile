FROM python:3-slim

WORKDIR /programas/ingesta

# Instalamos dependencias necesarias
RUN pip3 install boto3 pymysql sqlalchemy cryptography pandas

COPY . .

CMD ["python3", "./ingesta.py"]

