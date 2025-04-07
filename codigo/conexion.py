# Volver al README:
https://github.com/Vaniirea/Proyecto-FaceMarket/blob/main/README.md


import pyodbc

def obtener_conexion_gestion_usuario():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost;'
        'DATABASE=FM_Clientes;'
        'Trusted_Connection=yes;'
    )
    return conn

def obtener_conexion_productos():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost;'
        'DATABASE=FM_Productos;'
        'Trusted_Connection=yes;'
    )
    return conn
