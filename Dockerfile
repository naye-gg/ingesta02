FROM python:3-slim

WORKDIR /programas/ingesta

COPY requirements.txt .
RUN pip3 install pymysql boto3 cryptography

COPY . .

CMD ["python3", "./ingesta.py"]

