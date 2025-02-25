import mysql.connector
from flood_nfip.config import *
import csv


def connect_to_mysql():
    try:
        return  mysql.connector.connect(**MYSQL_CONFIG)
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        raise



def list_databases_and_tables():
    """List all databases and their tables."""
    try:
        connection = connect_to_mysql()
        cursor = connection.cursor()

        # Fetch and print all databases
        cursor.execute("SHOW DATABASES;")
        databases = cursor.fetchall()
        print("Databases:")
        for db in databases:
            print(f"- {db[0]}")

        # Fetch tables from each database
        for db in databases:
            db_name = db[0]
            print(f"\nTables in database `{db_name}`:")

            cursor.execute(f"USE {db_name};")  # Switch to the database
            cursor.execute("SHOW TABLES;")  # Get tables
            tables = cursor.fetchall()

            if not tables:
                print("  (No tables found)")
            else:
                for table in tables:
                    print(f"  - {table[0]}")

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error retrieving databases or tables: {err}")


def ping_table(connection, db_name, table_name):
    try:
        cursor = connection.cursor()
        cursor.execute(f"USE {db_name};")
        cursor.execute(f"SHOW TABLES LIKE '{table_name}';") 
        result = cursor.fetchone()  
        if result:  print(f"Table '{table_name}' exists!")
        else: print(f"Table '{table_name}' does not exist!")
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error during query execution: {err}")

def list_tables(cursor):
    """Print all tables in the specified database."""
    # cursor.execute(f"USE {database};")
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()

    print("\n Current Tables in Database:")
    if tables:
        for table in tables:
            print(f"  - {table[0]}")
    else:
        print("  (No tables found)")
    return tables

def create_table_from_csv(csv_file,db_name, table_name):
    try:
        connection = connect_to_mysql()
        cursor = connection.cursor()
        cursor.execute(f"USE {db_name};")
        tables = list_tables(cursor)
        for table in tables:
            if table_name.lower() == table[0]:
                print("Skipping creation, table already initialized")
                cursor.close()
                connection.close()
                return
            

        with open(csv_file, mode='r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader) 

        column_types = {
            "latitude": "FLOAT",
            "longitude": "FLOAT",
            "amountPaidOnBuildingClaim": "DECIMAL(12,2)",
            "amountPaidOnContentsClaim": "DECIMAL(12,2)",
            "amountPaidOnIncreasedCostOfComplianceClaim": "DECIMAL(12,2)",
            "netBuildingPaymentAmount": "DECIMAL(12,2)",
            "netContentsPaymentAmount": "DECIMAL(12,2)",
            "netIccPaymentAmount": "DECIMAL(12,2)",
            "buildingReplacementCost": "DECIMAL(12,2)",
            "contentsReplacementCost": "DECIMAL(12,2)",
            "waterDepth": "DECIMAL(5,2)",
            "nfipCommunityName": "TEXT",
            "floodEvent": "TEXT",
            "reportedCity": "TEXT",
            "reportedZipCode": "VARCHAR(20)",
            "countyCode": "VARCHAR(20)",
            "censusTract": "VARCHAR(50)",
            "censusBlockGroupFips": "VARCHAR(50)"
        }

        # Construct CREATE TABLE query
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
        for column in header:
            column_name = column.replace(" ", "_")  # Ensure column names are valid
            column_type = column_types.get(column_name, "VARCHAR(255)")  # Use default if not specified
            create_table_query += f"{column_name} {column_type}, "

        create_table_query = create_table_query.rstrip(", ") + ");"

        cursor.execute(create_table_query)
        print(f"Table {table_name} created successfully.")
        list_tables(cursor)
        
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error during table creation: {err}")


def clean_row(row):
    """Convert empty strings to NULL for MySQL."""
    return [None if value == '' else value for value in row]


def csv_row_generator(csv_file):
    """generotar function to yield header and rows from big csv file"""
    with open(csv_file, mode = 'r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader) #first row is headers
        yield header #yield headers first
        for row in csv_reader:
            yield row #then yield row by row

def import_csv_to_mysql(csv_file, db_name, table_name):
    try:
        connection = connect_to_mysql()
        cursor = connection.cursor()
        read_data = csv_row_generator(csv_file)
        headers = next(read_data)

        insert_query = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({' ,'.join(['%s'] * len(headers))});"
        batch_size = 1000
        batch = []
        for row in read_data:
            cleaned_row = clean_row(row)
            batch.append(cleaned_row)
            if len(batch) >= batch_size:
                #load batch 
                cursor.executemany(insert_query, batch)
                cursor.commit()
                print(f"Inserted {batch_size} rows...")
                batch = [] #reset batch list 
        #if batch still remaining aka last batch less than batch size
        if batch:
            cursor.executemany(insert_query, batch)
            cursor.commit()
            print(f"Inserted final {len(batch)} rows.")
        cursor.execute(f"SHOW TABLE STATUS WHERE Name='{table_name}'")
        cursor.close()
        connection.close()
    except mysql.connection.Error as err:
        print(f"Data import error during loading from csv into SQL {err}")

def import_csv_to_mysql(csv_file,db_name, table_name):
    try:
        connection = connect_to_mysql()
        cursor = connection.cursor()

        with open(csv_file, mode='r') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader) 

            #creating template query for mysql.connection.cursor.executemany to utilize
            insert_query = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({', '.join(['%s'] * len(headers))});"
            

            # Process and insert rows in batches
            batch_size = 1000
            batch = []

            for row in csv_reader:
                cleaned_row = clean_row(row)
                batch.append(cleaned_row)

                if len(batch) >= batch_size:
                    cursor.executemany(insert_query, batch)  # Execute batch insert
                    connection.commit()
                    print(f"✅ Inserted {len(batch)} rows...")
                    batch = []

            # Insert any remaining rows
            if batch:
                cursor.executemany(insert_query, batch)
                connection.commit()
                print(f"✅ Inserted final {len(batch)} rows.")
        
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error during import: {err}")

def is_table_empty(db_name, table_name):
    """Check if a table is empty in MySQL."""
    try:
        connection = connect_to_mysql()
        cursor = connection.cursor()

        cursor.execute(f"SHOW TABLES LIKE '{table_name}';")
        if not cursor.fetchall():
            print(f"⚠️ Table `{table_name}` is EMPTY. Not yet initialized.")
            return True

        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        row_count = cursor.fetchone()[0]

        cursor.execute(f"SHOW COLUMNS FROM {table_name};")
        col_count = len(cursor.fetchall())

        cursor.close()
        connection.close()

        if row_count > 0:
            print(f"✅ Table `{table_name}` is NOT empty. It has {row_count} rows and {col_count} columns.")
            return False
        else:
            print(f"⚠️ Table `{table_name}` is EMPTY. Initialized but not loaded.")
            return True

    except mysql.connector.Error as err:
        print(f"❌ Error checking table: {err}")
        return None



def fetch_sample_row(table_name, row_count = 1):
    """Print first 3 rows in SQL table."""
    try:
        connection = connect_to_mysql()
        cursor = connection.cursor()
       
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {row_count};")
        rows = cursor.fetchall()
        # columns = [desc[0] for desc in cursor.description]

        cursor.execute(f"SHOW COLUMNS FROM {table_name};")
        headers = cursor.fetchall()
        column_names = [col[0] for col in headers]
        column_types = {col[0]: col[1] for col in headers}


        cursor.close()
        connection.close()

        return rows, column_names, column_types
    except mysql.connector.Error as err:
        print(f"❌ Error fetching rows: {err}")
        return None
