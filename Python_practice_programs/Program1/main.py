import mysql.connector
import csv

def get_connection():
    """Establish connection to the MySQL database."""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="####",   # replace with your MySQL password
        database="employees"
    )
    return connection


def get_basic_data(cursor):
    """Run simple queries and print basic info."""
    # 1. Count employees
    cursor.execute("SELECT COUNT(*) FROM employees;")
    print("Total employees:", cursor.fetchone()[0])

    # 2. Find employees hired after 2000
    cursor.execute("SELECT first_name, last_name, hire_date FROM employees WHERE hire_date > '2000-01-01' LIMIT 10;")
    print("\nEmployees hired after 2000:")
    for row in cursor.fetchall():
        print(row)

    # 3. Average salary
    cursor.execute("SELECT AVG(salary) FROM salaries;")
    print("\nAverage salary:", cursor.fetchone()[0])


def fetch_large_query(cursor, query, batch_size=10000):
    """Generator to fetch query results in small batches."""
    cursor.execute(query)
    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        for row in rows:
            yield row  # yield one record at a time


def export_to_csv(cursor, query, filename="salaries_output.csv"):
    """Fetch large query results and save them into a CSV file."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write header
        header = [desc[0] for desc in cursor.description]
        writer.writerow(header)

        count = 0
        for record in fetch_large_query(cursor, query):
            writer.writerow(record)
            count += 1

        print(f"\n✅ Export complete. {count} records saved to '{filename}'.")


# ----------------- MAIN EXECUTION -----------------
if __name__ == "__main__":
    try:
        connection = get_connection()
        cursor = connection.cursor()

        get_basic_data(cursor)

        # Export large table data
        export_to_csv(cursor, "SELECT * FROM salaries;", "salaries_data.csv")

    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("\n✅ MySQL connection closed.")
