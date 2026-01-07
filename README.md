# Asana RL Seed Data Generator

This repository contains a system for generating realistic, enterprise-grade seed data
to simulate an Asana workspace for reinforcement learning (RL) environments.

The project focuses on data realism, relational consistency, and evidence-based
generation strategies suitable for evaluating computer-use AI agents.

---

## Project Overview

The simulated environment represents a B2B SaaS organization with 5,000–10,000 employees
using Asana across engineering, product, marketing, and operations workflows.

The generated dataset includes:
- Organizations and users
- Teams and team memberships
- Projects and workflow sections
- Tasks, subtasks, comments
- Tags and project-scoped custom fields

The output is a fully populated SQLite database that mirrors real-world Asana usage patterns.

---

## Repository Structure

```
schema.sql            # Relational schema (SQLite)
src/main.py           # Entry point and orchestration
src/generators/       # Data generation modules
prompts/              # LLM prompt templates (if applicable)
output/               # Generated SQLite database
```

---

## Setup Instructions

### 1. Create a virtual environment (optional)

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run data generation

```bash
python src/main.py
```

This will create `output/asana_simulation.sqlite`.

---

## Design Principles

- Non-uniform, realistic distributions
- Referential and temporal consistency
- Modular and extensible generator design
- Separation of schema, logic, and orchestration

---

## Notes

This repository is part of a take-home assignment for a Research Scientist Internship
and is intended to demonstrate data design and generation methodology rather than
model training.
