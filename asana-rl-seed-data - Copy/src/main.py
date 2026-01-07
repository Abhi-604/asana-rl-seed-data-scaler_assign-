
import os
import sqlite3

from generators.users import generate_users
from generators.teams import generate_teams, generate_team_memberships
from generators.projects import generate_projects_and_sections
from generators.tasks import generate_tasks


# =========================
# Configuration
# =========================
DB_PATH = "output/asana_simulation.sqlite"
RECREATE_DB = True   # Set False if you want incremental runs (not recommended)
NUM_USERS = 5000
NUM_TEAMS = 200


# =========================
# Database Initialization
# =========================
def initialize_db(conn):
    """
    Create database schema from schema.sql
    """
    with open("schema.sql", "r") as f:
        schema = f.read()
    conn.executescript(schema)
    conn.commit()


# =========================
# Main Orchestration
# =========================
def main():

    # Clean regeneration (recommended for simulations)
    if RECREATE_DB and os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)

    # Initialize schema only once per run
    initialize_db(conn)

    # Create organization (root entity)
    org_id = "org-1"
    conn.execute(
        """
        INSERT INTO organizations (id, name, created_at)
        VALUES (?, ?, datetime('now'))
        """,
        (org_id, "Example SaaS Company")
    )
    conn.commit()

    # -------------------------
    # Data Generation Pipeline
    # -------------------------

    # 1. Users
    generate_users(conn, org_id, num_users=NUM_USERS)

    # 2. Teams + memberships
    team_ids = generate_teams(conn, org_id, num_teams=NUM_TEAMS)
    generate_team_memberships(conn, team_ids)

    generate_projects_and_sections(conn)
    generate_tasks(conn)



    conn.close()
    print("✅ Asana simulation database generated successfully.")


if __name__ == "__main__":
    main()
