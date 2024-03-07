import pyodbc

conn = pyodbc.connect (
    "Driver={SQL Server};"
    "Server=DESKTOP-HK8D59P\SQLEXPRESS;"
    "Database=RocketDB;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

velocity = 'velocity_meters_per_second'
altitude = 'altitude_meters'
temp = 'temperature_celsius'
pressure = 'pressure_pascals'
fuel = 'fuel_consumption'
weight = 'weight_newtons'


def print_table_data(table):
    try:

        
        cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'{table}'")
        columns = [row.COLUMN_NAME for row in cursor.fetchall()]

        
        print("\nColumn names and data:\n")
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        for row in rows:
            for column, value in zip(columns, row):
                print(f"{column}: {value}", end="\n\n")
            print()
    
    except pyodbc.Error as e:
        print("Error printing table data:", e)

def read(query):
    cursor = conn.cursor()
    cursor.execute(f"select * from {query}")
    for row in cursor:
        print(f'row = {row}')
    print()

def insert(table, *values):
    try:

        # Get the column names
        cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'{table}'")
        columns = [row.COLUMN_NAME for row in cursor.fetchall()]

        # Prepare the SQL statement with parameterized query
        sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['?' for _ in columns])})"

        # Execute the insert statement with the provided values
        cursor.execute(sql, values)
        conn.commit()
        print("Insert successful")

    except pyodbc.Error as e:
        print("Error inserting into database:", e)
        conn.rollback()

def alter_table_add_column(table, column_name, data_type):
    try:

        # Prepare the SQL statement to add a new column
        sql = f"ALTER TABLE {table} ADD {column_name} {data_type}"

        # Execute the alter table statement
        cursor.execute(sql)
        conn.commit()
        print("Alter table successful")

    except pyodbc.Error as e:
        print("Error altering table:", e)
        conn.rollback()
    finally:
        # Close the connection
        conn.close()

def update(column, new_value):
    try:
        
        sql = f"UPDATE telemetry SET {column} = ? WHERE {'telemetry_ID'} = 24601"

        cursor.execute(sql, (new_value))
        conn.commit()

    except pyodbc.Error as e:
        print("Error updating value in database:", e)
        conn.rollback()


update(velocity, 5000)



print_table_data('telemetry')
