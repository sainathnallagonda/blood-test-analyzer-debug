import sqlite3
import csv

# Connect to your database
conn = sqlite3.connect('analysis_results.db')
cursor = conn.cursor()

# Query all data from the table
try:
    cursor.execute("SELECT * FROM analysis_results")
    rows = cursor.fetchall()
    # Get column names
    column_names = [description[0] for description in cursor.description]

    # Write to CSV
    with open('analysis_results_export.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(column_names)
        writer.writerows(rows)
    print("Exported analysis_results to analysis_results_export.csv")
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()
