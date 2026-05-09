from sqlalchemy import inspect
from conexion import engine

insp = inspect(engine)

tablas = insp.get_table_names()

print("Tablas en Store2:")

for tabla in tablas:
    print("-", tabla)