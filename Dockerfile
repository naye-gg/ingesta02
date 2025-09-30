FROM python:3-slim

WORKDIR /programas/ingesta


RUN pip3 install pandas sqlalchemy pymysql boto3 cryptography

COPY . .

CMD ["python3", "./ingesta.py"]

