import uuid
import random
from datetime import datetime, timedelta


# =========================
# Task Name Templates
# =========================

ENGINEERING_TASKS = [
    "Auth Service - Fix token refresh bug",
    "API Gateway - Improve error handling",
    "Payments - Add retry logic",
    "Search - Optimize query performance",
    "Notifications - Handle retry failures",
]

MARKETING_TASKS = [
    "Q2 Launch - Landing page copy",
    "Email Campaign - Draft subject lines",
    "Product Blog - Final review",
    "Social Media - Schedule posts",
    "Ad Campaign - Performance analysis",
]

OPS_TASKS = [
    "Onboarding - Update checklist",
    "Incident Response - Postmortem",
    "Compliance - Review access logs",
    "Hiring - Interview coordination",
    "IT Ops - Access provisioning",
]


# =========================
# Tags
# =========================

TAGS = ["urgent", "backend", "frontend", "design", "blocked", "high-priority"]


# =========================
# Helpers
# =========================

def random_due_date():
    r = random.random()
    today = datetime.now()

    if r < 0.10:
        return None
    elif r < 0.35:
        return today + timedelta(days=random.randint(1, 7))
    elif r < 0.75:
        return today + timedelta(days=random.randint(8, 30))
    elif r < 0.95:
        return today + timedelta(days=random.randint(31, 90))
    else:
        return today - timedelta(days=random.randint(1, 14))  # overdue


# =========================
# Main Generator
# =========================

def generate_tasks(conn):
    cursor = conn.cursor()

    # Insert tags once
    cursor.execute("SELECT COUNT(*) FROM tags")
    if cursor.fetchone()[0] == 0:
        for tag in TAGS:
            cursor.execute(
                "INSERT INTO tags (id, name) VALUES (?, ?)",
                (str(uuid.uuid4()), tag)
            )
    conn.commit()

    cursor.execute("SELECT id, name FROM tags")
    tag_ids = [row[0] for row in cursor.fetchall()]

    # Fetch projects
    cursor.execute("""
        SELECT p.id, p.project_type, p.team_id
        FROM projects p
    """)
    projects = cursor.fetchall()

    for project_id, project_type, team_id in projects:

        # Task volume & completion rate
        if project_type == "engineering_sprint":
            num_tasks = random.randint(30, 80)
            completion_rate = random.uniform(0.7, 0.85)
            name_pool = ENGINEERING_TASKS
            custom_fields = {
                "Priority": ["Low", "Medium", "High"],
                "Effort": ["1", "2", "3", "4", "5"]
            }
        elif project_type == "marketing_campaign":
            num_tasks = random.randint(15, 40)
            completion_rate = random.uniform(0.5, 0.65)
            name_pool = MARKETING_TASKS
            custom_fields = {
                "Channel": ["Email", "Social", "Paid"]
            }
        else:
            num_tasks = random.randint(10, 30)
            completion_rate = random.uniform(0.4, 0.55)
            name_pool = OPS_TASKS
            custom_fields = {}

        # Team members
        cursor.execute("""
            SELECT u.id
            FROM users u
            JOIN team_memberships tm ON u.id = tm.user_id
            WHERE tm.team_id = ?
        """, (team_id,))
        team_users = [row[0] for row in cursor.fetchall()]

        # Sections
        cursor.execute("""
            SELECT id FROM sections
            WHERE project_id = ?
        """, (project_id,))
        sections = [row[0] for row in cursor.fetchall()]

        # Create custom fields for project
        field_ids = {}
        for field_name, options in custom_fields.items():
            field_id = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO custom_fields (id, name, field_type, project_id)
                VALUES (?, ?, ?, ?)
            """, (field_id, field_name, "enum", project_id))
            field_ids[field_id] = options

        # Generate tasks
        for _ in range(num_tasks):
            task_id = str(uuid.uuid4())
            created_at = datetime.now() - timedelta(days=random.randint(1, 120))
            due_date = random_due_date()

            assignee_id = (
                random.choice(team_users)
                if team_users and random.random() > 0.15
                else None
            )

            completed = random.random() < completion_rate
            completed_at = (
                created_at + timedelta(days=random.randint(1, 14))
                if completed else None
            )

            task_name = random.choice(name_pool)

            cursor.execute("""
                INSERT INTO tasks (
                    id, name, description, assignee_id,
                    project_id, section_id, due_date,
                    completed, created_at, completed_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task_id,
                task_name,
                None,
                assignee_id,
                project_id,
                random.choice(sections),
                due_date.date() if due_date else None,
                completed,
                created_at,
                completed_at
            ))

            # Assign tags
            for tag_id in random.sample(tag_ids, random.randint(0, 3)):
                cursor.execute("""
                    INSERT INTO task_tags (task_id, tag_id)
                    VALUES (?, ?)
                """, (task_id, tag_id))

            # Assign custom field values
            for field_id, options in field_ids.items():
                cursor.execute("""
                    INSERT INTO custom_field_values (task_id, custom_field_id, value)
                    VALUES (?, ?, ?)
                """, (task_id, field_id, random.choice(options)))

            # Subtasks
            if random.random() < 0.4:
                for _ in range(random.randint(2, 5)):
                    cursor.execute("""
                        INSERT INTO subtasks (
                            id, parent_task_id, name,
                            completed, created_at
                        )
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        str(uuid.uuid4()),
                        task_id,
                        "Subtask - " + random.choice(name_pool),
                        completed and random.random() < 0.8,
                        created_at
                    ))

            # Comments
            if team_users and random.random() < 0.5:
                for _ in range(random.randint(1, 4)):
                    cursor.execute("""
                        INSERT INTO comments (
                            id, task_id, author_id,
                            content, created_at
                        )
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        str(uuid.uuid4()),
                        task_id,
                        random.choice(team_users),
                        "Discussion / status update",
                        created_at + timedelta(days=random.randint(0, 10))
                    ))

    conn.commit()
