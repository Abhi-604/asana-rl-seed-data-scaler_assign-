import uuid
import random
from datetime import datetime

TEAM_TYPES = [
    "Engineering",
    "Product",
    "Marketing",
    "Sales",
    "Operations",
    "HR",
    "Finance"
]

def generate_teams(conn, organization_id, num_teams=200):
    cursor = conn.cursor()
    team_ids = []

    for i in range(num_teams):
        team_id = str(uuid.uuid4())
        team_type = random.choice(TEAM_TYPES)
        team_name = f"{team_type} Team {i+1}"

        cursor.execute("""
            INSERT INTO teams (id, name, organization_id, created_at)
            VALUES (?, ?, ?, ?)
        """, (team_id, team_name, organization_id, datetime.now()))

        team_ids.append(team_id)

    conn.commit()
    return team_ids


def generate_team_memberships(conn, team_ids):
    cursor = conn.cursor()

    cursor.execute("SELECT id, role FROM users")
    users = cursor.fetchall()

    for user_id, role in users:
        # Every user has one primary team
        primary_team = random.choice(team_ids)
        cursor.execute("""
            INSERT INTO team_memberships (user_id, team_id, joined_at)
            VALUES (?, ?, datetime('now'))
        """, (user_id, primary_team))

        # Some users (esp managers) have a second team
        if role in ["Manager", "Director"] and random.random() < 0.4:
            secondary_team = random.choice(team_ids)
            if secondary_team != primary_team:
                cursor.execute("""
                    INSERT OR IGNORE INTO team_memberships (user_id, team_id, joined_at)
                    VALUES (?, ?, datetime('now'))
                """, (user_id, secondary_team))

    conn.commit()
