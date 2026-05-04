from app.db import get_cursor

conn, cursor = get_cursor()

cursor.execute("SELECT 1;")
print(cursor.fetchone())

cursor.close()
conn.close()