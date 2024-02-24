import pyodbc



def read(query):
    cursor = conn.cursor()
    cursor.execute(f"select * from {query}")
    for row in cursor:
        print(f'row = {row}')
    print()


conn = pyodbc.connect (
    "Driver={SQL Server};"
    "Server=DESKTOP-HK8D59P\SQLEXPRESS;"
    "Database=RocketDB;"
    "Trusted_Connection=yes;"

)

cursor = conn.cursor()


read('rocket')