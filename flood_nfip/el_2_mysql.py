import mysql.connector
from flood_nfip.config import *
import flood_nfip.utils_sql as utils_sql

import csv





def main():
    try:
        # list_databases_and_tables()
        connection = utils_sql.connect_to_mysql()
        if connection:
            utils_sql.ping_table(connection, MYSQL_DB_NAME, MYSQL_TABLE_NAME)
            # Create the table dynamically based on the CSV file
            utils_sql.create_table_from_csv(ORIGINAL_PATH, MYSQL_DB_NAME, MYSQL_TABLE_NAME)

            if utils_sql.is_table_empty(MYSQL_DB_NAME, MYSQL_TABLE_NAME):
                utils_sql.import_csv_to_mysql(ORIGINAL_PATH, MYSQL_TABLE_NAME)
            else:
                sample_row, headers, header_types = utils_sql.fetch_sample_row(MYSQL_TABLE_NAME)
                print(f"Data loaded in SQL server at {MYSQL_TABLE_NAME}")
                for row in sample_row:
                    for col, val in zip(headers, row):
                        print(f"{header_types[col]} {col}: {type(val)} {val}")

            
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()


"""
connection = mysql.connection.connect(**MYSQL_ACCESS_CONFIG)
cursor=connection.cursor()
cursor.execute(query)
cursor.executemany(query_template, list_of_rows)
cursor.commit()
cursor.close()
connection.close()

#assuming **config specified database
q1 = "SHOW TABLES LIKE '{table}';"
q2 = "SELECT * FROM {table};"
q3 " "SHOW COLUMNS FROM {table};"
q4 = "INSERT INTO {table} (h1, h2) VALUES (v1, v2);"
q5 = "INSERT INTO {table} (", ".join(headers)) VALUES (", ".join( ['%s' * len(headers)) ]);" 
"""