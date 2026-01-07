import sqlite3
from generators.users import generate_users

def initialize_db(conn):
    with open("schema.sql", "r") as f:
        schema = f.read()
    conn.executescript(schema)
    conn.commit()

def main():
    conn = sqlite3.connect("output/asana_simulation.sqlite")

    # IMPORTANT: create tables first
    initialize_db(conn)

    org_id = "org-1"

    # Insert organization first (users depend on it)
    conn.execute(
        "INSERT OR IGNORE INTO organizations (id, name, created_at) VALUES (?, ?, datetime('now'))",
        (org_id, "Example SaaS Company")
    )
    conn.commit()

    generate_users(conn, org_id, num_users=5000)

    conn.close()

if __name__ == "__main__":
    main()
