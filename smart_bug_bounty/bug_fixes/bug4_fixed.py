import sqlite3

def find_user_by_username(cursor, username):
    query = "SELECT id, username, role FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    return cursor.fetchone()

if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, role TEXT)")
    cursor.execute("INSERT INTO users VALUES (1, 'guest', 'user')")
    cursor.execute("INSERT INTO users VALUES (2, 'admin', 'administrator')")
    conn.commit()

    t1 = find_user_by_username(cursor, "admin")
    print(f"Test 1 (Legitimate Query): {'PASS' if t1 and t1[1] == 'admin' else 'FAIL'}")

    t2 = find_user_by_username(cursor, "guest' OR role = 'administrator")
    print(f"Test 2 (SQL Injection Blocked): {'PASS' if t2 is None else 'FAIL'}")

    t3 = find_user_by_username(cursor, "unknown_user")
    print(f"Test 3 (Nonexistent User): {'PASS' if t3 is None else 'FAIL'}")

    conn.close()
