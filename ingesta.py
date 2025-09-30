#!/usr/bin/env python3
# ingesta.py
import os
import csv
import pymysql
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# Config desde environment vars con valores por defecto
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", 5433))
DB_USER = os.getenv("DB_USER", "mysql_ingesta")
DB_PASS = os.getenv("DB_PASS", "utec")
DB_NAME = os.getenv("DB_NAME", "ingestaDB")
TABLE_NAME = os.getenv("TABLE_NAME", "data")

CSV_FILENAME = os.getenv("CSV_FILENAME", "exported_data.csv")

S3_BUCKET = os.getenv("S3_BUCKET", "ingesta02-bucket-naye")
S3_KEY = os.getenv("S3_KEY", CSV_FILENAME)

def fetch_all_from_table():
    conn = None
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            cursorclass=pymysql.cursors.Cursor,
            connect_timeout=10
        )
        with conn.cursor() as cur:
            sql = f"SELECT * FROM `{TABLE_NAME}`;"
            cur.execute(sql)
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]
            return cols, rows
    finally:
        if conn:
            conn.close()

def write_csv(columns, rows, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)

def upload_to_s3(filename, bucket, key):
    s3 = boto3.client("s3")
    try:
        s3.upload_file(filename, bucket, key)
        print(f"✅ Archivo subido a s3://{bucket}/{key}")
    except (BotoCoreError, ClientError) as e:
        print("Error subiendo a S3:", e)
        raise

def main():
    print("Configuración:")
    print(f" DB -> {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME} , tabla='{TABLE_NAME}'")
    print(f" CSV -> {CSV_FILENAME}")
    print(f" S3 -> bucket='{S3_BUCKET}' key='{S3_KEY}'")

    cols, rows = fetch_all_from_table()
    if not rows:
        print("⚠️ Advertencia: la consulta no devolvió filas (tabla vacía o no existe).")
    else:
        print(f"Se obtuvieron {len(rows)} filas.")

    write_csv(cols, rows, CSV_FILENAME)
    print(f"✅ CSV generado: {CSV_FILENAME}")

    upload_to_s3(CSV_FILENAME, S3_BUCKET, S3_KEY)
    print("Ingesta completada.")

if __name__ == "__main__":
    main()

