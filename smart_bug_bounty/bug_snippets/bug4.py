import sqlite3

def find_user_by_username(cursor, username):
    query = f"SELECT id, username, role FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()

if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, role TEXT)")
    cursor.execute("INSERT INTO users VALUES (1, 'guest', 'user')")
    cursor.execute("INSERT INTO users VALUES (2, 'admin', 'administrator')")
    conn.commit()

    payload = "guest' OR role = 'administrator"
    res = find_user_by_username(cursor, payload)
    print("User retrieved:", res)
    conn.close()
