import pandas as pd
from sqlalchemy import create_engine

# Conexión
engine = create_engine("mysql+pymysql://mysql_ingesta:utec@172.31.39.193:5433/ingestaDB")

# Leer CSV
df = pd.read_csv("data.csv")

# Insertar en la tabla 'data'
df.to_sql("data", engine, if_exists="replace", index=False)

