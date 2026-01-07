import uuid
import random
from datetime import datetime

PROJECT_TYPES = {
    "Engineering": "engineering_sprint",
    "Product": "product_initiative",
    "Marketing": "marketing_campaign",
    "Sales": "sales_pipeline",
    "Operations": "operational_workflow",
    "HR": "operational_workflow",
    "Finance": "operational_workflow",
}

SECTION_TEMPLATES = {
    "engineering_sprint": ["Backlog", "In Progress", "Review", "Done"],
    "product_initiative": ["Ideas", "Planned", "In Progress", "Done"],
    "marketing_campaign": ["Ideas", "Planned", "Executing", "Launched"],
    "sales_pipeline": ["Leads", "Qualified", "Negotiation", "Closed"],
    "operational_workflow": ["To Do", "In Progress", "Blocked", "Done"],
}


def generate_projects_and_sections(conn, num_projects_per_team=(3, 7)):
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM teams")
    teams = cursor.fetchall()

    project_ids = []

    for team_id, team_name in teams:
        team_type = team_name.split()[0]
        project_type = PROJECT_TYPES.get(team_type, "operational_workflow")

        num_projects = random.randint(*num_projects_per_team)

        for _ in range(num_projects):
            project_id = str(uuid.uuid4())
            project_name = f"{team_type} Project {_+1}"

            cursor.execute("""
                INSERT INTO projects (id, name, team_id, project_type, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (project_id, project_name, team_id, project_type, datetime.now()))

            sections = SECTION_TEMPLATES[project_type]
            for pos, section_name in enumerate(sections):
                cursor.execute("""
                    INSERT INTO sections (id, name, project_id, position)
                    VALUES (?, ?, ?, ?)
                """, (
                    str(uuid.uuid4()),
                    section_name,
                    project_id,
                    pos
                ))

            project_ids.append(project_id)

    conn.commit()
    return project_ids
