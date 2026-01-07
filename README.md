# Asana RL Seed Data Generator

This repository contains a **realistic, enterprise-grade seed data generation framework** for simulating an **Asana-like workspace** to support **reinforcement learning (RL) environments**.

The project focuses on **data realism**, **relational consistency**, and **reproducible generation** of large-scale organizational workflows, suitable for evaluating computer-use AI agents in enterprise project management scenarios.

---

## 📌 Project Overview

The simulated environment represents a **B2B SaaS organization** with **5,000–10,000 employees** using Asana across:

- Engineering
- Product
- Marketing
- Operations (HR, Finance, IT)

The output is a **fully populated SQLite database** that mirrors real-world Asana usage patterns, including collaboration, task workflows, metadata, and edge cases.

---

## 🗂️ Features

The generated dataset includes:

- Organizations and users  
- Teams and team memberships (many-to-many)  
- Projects mapped to teams  
- Workflow sections per project  
- Tasks with realistic distributions  
- Subtasks and hierarchical task structure  
- Comments simulating collaboration  
- Tags for cross-project labeling  
- Project-scoped custom fields (priority, effort, channel, etc.)

---

## 🧱 Repository Structure

```
schema.sql                  # Relational database schema (SQLite)
README.md                   # Project documentation
requirements.txt            # Python dependencies
src/
├── main.py                 # Orchestration entry point
├── generators/
│   ├── users.py            # User generation
│   ├── teams.py            # Teams and memberships
│   ├── projects.py         # Projects and sections
│   ├── tasks.py            # Tasks, subtasks, comments, tags, custom fields
├── utils/                  # Helper utilities
prompts/                    # LLM prompt templates (optional / extensible)
output/
└── asana_simulation.sqlite # Generated database
```

---

## ⚙️ Setup Instructions

### 1️⃣ (Optional) Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run data generation

```bash
python src/main.py
```

This will generate the SQLite database at:

```
output/asana_simulation.sqlite
```

---

## 📦 Database Access

Due to file size constraints, the generated SQLite database is not stored directly in the repository.

The final database file (`asana_simulation.sqlite`) can be downloaded from the following link:

https://drive.google.com/file/d/1HmBxZtQc4x0ne_uX45DlpGTR8bPRKvEO/view?usp=sharing

After downloading, place the file in:

```
output/asana_simulation.sqlite
```

Alternatively, the database can be regenerated locally by running:

```bash
python src/main.py
```

## 🔁 Reproducibility & Design Choices

- The database is **regenerated from scratch on each run** to ensure consistency.
- Non-uniform distributions are used to reflect real enterprise behavior.
- Edge cases such as:
  - Unassigned tasks  
  - Overdue tasks  
  - Stalled projects  
  are intentionally included to prevent shortcut learning in RL agents.
- Schema design follows relational best practices with strict foreign key usage.

---

## 🎯 Intended Use

This dataset is designed to serve as **seed data** for:

- Reinforcement learning environments  
- Simulation-based evaluation of computer-use agents  
- Research on workflow automation and task navigation  

It is **not** intended for direct model training, but as a **high-fidelity environment substrate**.

---

## 📝 Notes

This repository was developed as part of a **Research Scientist Internship take-home assignment** and is intended to demonstrate:

- System and schema design  
- Realistic data generation methodology  
- Research-oriented engineering practices  

---

## ✅ Status

✔ Core schema implemented  
✔ Realistic large-scale data generated  
✔ Reproducible and extensible pipeline  
✔ Submission-ready and interview-ready  

---

## 📬 Contact

For questions regarding the design or methodology, please refer to the accompanying documentation provided in the submission.
