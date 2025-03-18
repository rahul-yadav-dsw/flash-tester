import psycopg2
import csv
import os
import random
import string

# Database configuration
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "123",
    "host": "localhost",
    "port": 5432,
}

# Function to ensure the table exists
def ensure_table_exists():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # Check if the table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'test_table1'
            );
        """)
        exists = cursor.fetchone()[0]

        # Create the table if it doesn't exist
        if not exists:
            cursor.execute("""
                CREATE TABLE test_table1 (
                    col1 VARCHAR(50),
                    col2 INTEGER,
                    col3 FLOAT
                );
            """)
            conn.commit()
            print("Table 'test_table1' created successfully.")
        else:
            print("Table 'test_table1' already exists.")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# Function to generate and save random data to a CSV file
def generate_csv_file(file_path, num_rows):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["col1", "col2", "col3"])  # Column headers
        for _ in range(num_rows):
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            random_int = random.randint(1, 1000)
            random_float = round(random.uniform(1.0, 100.0), 2)
            writer.writerow([random_string, random_int, random_float])

# Load CSV into PostgreSQL using COPY
def copy_csv_to_postgres(file_path, table_name):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        with open(file_path, 'r') as f:
            cursor.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV HEADER", f)
        conn.commit()
        print(f"Data from {file_path} inserted into {table_name} successfully.")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Ensure the table exists before inserting data
    ensure_table_exists()

    # Generate and insert 1 million rows using COPY
    table_name = "test_table1"
    csv_file_path = "data.csv"
    
    generate_csv_file(csv_file_path, 1000000)  # Generate CSV with 1M rows
    copy_csv_to_postgres(csv_file_path, table_name)

    # Clean up the CSV file after insertion (optional)
    os.remove(csv_file_path)
