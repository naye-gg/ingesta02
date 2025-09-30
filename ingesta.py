import boto3
import pymysql
import csv

# Configuración de MySQL
db_config = {
    "host": "tu_host_mysql",
    "user": "tu_usuario",
    "password": "tu_password",
    "database": "tu_bd"
}

# Configuración S3
ficheroUpload = "data.csv"
nombreBucket = "gcr-output-01"

# 1. Conexión a MySQL
connection = pymysql.connect(**db_config)

try:
    with connection.cursor() as cursor:
        # Cambia "mi_tabla" por tu tabla real
        cursor.execute("SELECT * FROM mi_tabla")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        # 2. Guardar en CSV
        with open(ficheroUpload, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(columns)  # encabezados
            writer.writerows(rows)

        print("CSV generado correctamente.")

finally:
    connection.close()

# 3. Subir a S3
s3 = boto3.client("s3")
s3.upload_file(ficheroUpload, nombreBucket, ficheroUpload)
print("Archivo subido a S3.")

