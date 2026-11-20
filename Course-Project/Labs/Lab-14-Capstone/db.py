import sqlite3
from pathlib import Path
from contextlib import contextmanager

DB_PATH = Path(__file__).resolve().parent / "internship_portal.db"

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with get_conn() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            full_name TEXT NOT NULL,
            student_id TEXT
        );
        CREATE TABLE IF NOT EXISTS students(
            student_id TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            department TEXT NOT NULL,
            cgpa REAL NOT NULL DEFAULT 0,
            backlogs INTEGER NOT NULL DEFAULT 0,
            credits INTEGER NOT NULL DEFAULT 0,
            skills TEXT NOT NULL DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS internships(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            department TEXT NOT NULL,
            description TEXT NOT NULL,
            required_skills TEXT NOT NULL,
            min_cgpa REAL NOT NULL DEFAULT 0,
            max_backlogs INTEGER NOT NULL DEFAULT 99,
            min_credits INTEGER NOT NULL DEFAULT 0,
            duration TEXT NOT NULL,
            mode TEXT NOT NULL,
            total_hours INTEGER NOT NULL DEFAULT 120,
            active INTEGER NOT NULL DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS applications(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            internship_id INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'Submitted',
            hod_status TEXT NOT NULL DEFAULT 'Pending',
            head_status TEXT NOT NULL DEFAULT 'Pending',
            student_note TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(student_id, internship_id),
            FOREIGN KEY(student_id) REFERENCES students(student_id),
            FOREIGN KEY(internship_id) REFERENCES internships(id)
        );
        CREATE TABLE IF NOT EXISTS offer_letters(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            uploaded_by TEXT NOT NULL,
            letter_type TEXT NOT NULL DEFAULT 'Uploaded',
            uploaded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(application_id) REFERENCES applications(id)
        );
        CREATE TABLE IF NOT EXISTS progress_logs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER NOT NULL,
            log_date TEXT NOT NULL,
            task_summary TEXT NOT NULL,
            hours REAL NOT NULL DEFAULT 0,
            learning TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(application_id) REFERENCES applications(id)
        );
        CREATE TABLE IF NOT EXISTS internship_marks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER NOT NULL UNIQUE,
            marks REAL NOT NULL,
            max_marks REAL NOT NULL DEFAULT 100,
            grade TEXT DEFAULT '',
            remarks TEXT DEFAULT '',
            marksheet_path TEXT DEFAULT '',
            updated_by TEXT NOT NULL,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(application_id) REFERENCES applications(id)
        );
        CREATE TABLE IF NOT EXISTS audit_logs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            actor TEXT NOT NULL,
            action TEXT NOT NULL,
            details TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Migrate databases created by earlier project versions.
        migrations = {
            "internships": {"total_hours": "INTEGER NOT NULL DEFAULT 120"},
            "applications": {
                "head_status": "TEXT NOT NULL DEFAULT 'Pending'",
            },
            "offer_letters": {
                "letter_type": "TEXT NOT NULL DEFAULT 'Uploaded'",
            },
        }
        for table, columns in migrations.items():
            existing = {r["name"] for r in c.execute(f"PRAGMA table_info({table})").fetchall()}
            for name, declaration in columns.items():
                if name not in existing:
                    c.execute(f"ALTER TABLE {table} ADD COLUMN {name} {declaration}")

        # Migrate old coordinator approval state into the new Internship Head field.
        old_cols = {r["name"] for r in c.execute("PRAGMA table_info(applications)").fetchall()}
        if "coordinator_status" in old_cols:
            c.execute("""
                UPDATE applications
                SET head_status=coordinator_status
                WHERE head_status='Pending' AND coordinator_status!='Pending'
            """)

def seed_data():
    from auth import hash_password
    students = [
        ("STU001", "Sangini Shee", "CS-AI", 8.4, 0, 150, "Python, ML, SQL, Data Analysis, TensorFlow"),
        ("STU002", "Sindhu Kesiraju", "CS-AI", 7.6, 0, 145, "Python, Java, Web Development, DBMS"),
        ("STU003", "Chirag Hanamaratti", "CS-AI", 6.5, 1, 130, "Java, Python, C++, Cloud"),
        ("STU004", "Kshitij Heblikar", "CS-AI", 7.0, 0, 140, "Python, ML, Deep Learning, Data Structures"),
    ]
    accounts = [
        ("sangini", "student123", "Student", "Sangini Shee", "STU001"),
        ("sindhu", "student123", "Student", "Sindhu Kesiraju", "STU002"),
        ("chirag", "student123", "Student", "Chirag Hanamaratti", "STU003"),
        ("kshitij", "student123", "Student", "Kshitij Heblikar", "STU004"),
        ("hod", "hod123", "HOD", "Demo HOD", None),
        ("internshiphead", "head123", "Internship Head", "Internship Head", None),
        ("admin", "admin123", "Admin", "Portal Administrator", None),
    ]
    with get_conn() as c:
        for record in students:
            c.execute("""
                INSERT INTO students(student_id,full_name,department,cgpa,backlogs,credits,skills)
                VALUES(?,?,?,?,?,?,?)
                ON CONFLICT(student_id) DO UPDATE SET full_name=excluded.full_name
            """, record)
        for username, password, role, full_name, student_id in accounts:
            existing = c.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
            if existing:
                c.execute(
                    "UPDATE users SET role=?,full_name=?,student_id=? WHERE username=?",
                    (role, full_name, student_id, username)
                )
            else:
                c.execute(
                    "INSERT INTO users(username,password_hash,role,full_name,student_id) VALUES(?,?,?,?,?)",
                    (username, hash_password(password), role, full_name, student_id)
                )

        count = c.execute("SELECT COUNT(*) n FROM internships").fetchone()["n"]
        if count == 0:
            c.executemany(
                """INSERT INTO internships(title,company,department,description,required_skills,
                   min_cgpa,max_backlogs,min_credits,duration,mode,total_hours)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                [
                    ("AI/ML Intern", "DemoTech Solutions", "Artificial Intelligence",
                     "Work on data preparation, model evaluation and ML prototypes.",
                     "Python, ML", 7.0, 0, 140, "3 months", "Hybrid", 120),
                    ("Software Development Intern", "Sample Innovations", "Software Engineering",
                     "Assist with backend APIs, testing and application development.",
                     "Python, Java", 6.0, 1, 120, "2 months", "Remote", 100),
                    ("Data Analyst Intern", "Demo Analytics", "Data Analytics",
                     "Clean datasets, write SQL queries and prepare reports.",
                     "SQL, Data Analysis", 6.5, 0, 130, "3 months", "On-site", 120),
                ]
            )

def audit(actor, action, details):
    with get_conn() as c:
        c.execute(
            "INSERT INTO audit_logs(actor,action,details) VALUES(?,?,?)",
            (actor, action, details)
        )
