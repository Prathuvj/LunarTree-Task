import sqlite3
import json
from datetime import datetime

DB_PATH = "jobs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            filename TEXT,
            company_name TEXT,
            github_members TEXT,
            status TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_job(job_id, filename, company_name=None, github_members=None, status="success"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    github_members_json = json.dumps(github_members) if github_members else None
    timestamp = datetime.now().replace(microsecond=0).isoformat()

    cursor.execute("""
        INSERT INTO jobs (id, filename, company_name, github_members, status, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (job_id, filename, company_name, github_members_json, status, timestamp))

    conn.commit()
    conn.close()