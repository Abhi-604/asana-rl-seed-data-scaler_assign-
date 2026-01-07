import uuid
import random
from datetime import datetime, timedelta

def generate_users(conn, organization_id, num_users):
    cursor = conn.cursor()

    roles = ["IC", "Manager", "Director"]
    role_weights = [0.7, 0.2, 0.1]

    for _ in range(num_users):
        user_id = str(uuid.uuid4())
        role = random.choices(roles, role_weights)[0]

        full_name = f"User {_}"
        email = f"user{_}@example.com"

        created_at = datetime.now() - timedelta(
            days=random.randint(30, 900)
        )

        cursor.execute("""
            INSERT INTO users (id, full_name, email, role, organization_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, full_name, email, role, organization_id, created_at))

    conn.commit()
