import sqlite3

try:
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM notes")
    print(cursor.fetchall())

    conn.close()

except Exception as e:
    print("ERROR:", e)