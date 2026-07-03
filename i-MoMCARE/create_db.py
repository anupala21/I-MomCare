import sqlite3

# Create Database Connection
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# =====================================
# USERS TABLE
# =====================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

# =====================================
# MOTHERS TABLE
# =====================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS mothers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mother_name TEXT NOT NULL,
    age INTEGER,
    weight REAL,
    bp TEXT,
    risk_level TEXT,
    pregnancy_week INTEGER,
    contact TEXT,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# =====================================
# CHILDREN TABLE
# =====================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS children(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    child_name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    weight REAL,
    height REAL,
    vaccination TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# =====================================
# APPOINTMENTS TABLE
# =====================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT NOT NULL,
    doctor_name TEXT NOT NULL,
    appointment_date TEXT NOT NULL,
    status TEXT DEFAULT 'Pending'
)
""")

# =====================================
# VACCINATION RECORDS TABLE
# =====================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS vaccination_records(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    child_name TEXT NOT NULL,
    vaccine_name TEXT NOT NULL,
    vaccination_date TEXT,
    next_due_date TEXT,
    status TEXT DEFAULT 'Pending'
)
""")

# =====================================
# MEDICAL RECORDS TABLE
# =====================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS medical_records(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT NOT NULL,
    diagnosis TEXT,
    prescription TEXT,
    doctor_name TEXT,
    visit_date TEXT
)
""")

# =====================================
# RISK ASSESSMENT TABLE
# =====================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS risk_assessment(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mother_name TEXT,
    age INTEGER,
    weight REAL,
    bp TEXT,
    risk_result TEXT,
    assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# =====================================
# NUTRITION RECORDS TABLE
# =====================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS nutrition_records(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mother_name TEXT,
    nutrition_plan TEXT,
    calories INTEGER,
    notes TEXT
)
""")

# =====================================
# HEALTH WORKERS TABLE
# =====================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS health_workers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    worker_name TEXT,
    phone TEXT,
    area TEXT
)
""")

# =====================================
# NOTIFICATIONS TABLE
# =====================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS notifications(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# =====================================
# COMMIT CHANGES
# =====================================

conn.commit()
conn.close()

print("=" * 50)
print(" i-MoMCARE DATABASE CREATED SUCCESSFULLY ")
print("=" * 50)

print("Tables Created:")
print("1. users")
print("2. mothers")
print("3. children")
print("4. appointments")
print("5. vaccination_records")
print("6. medical_records")
print("7. risk_assessment")
print("8. nutrition_records")
print("9. health_workers")
print("10. notifications")

print("=" * 50)
print("Database File Created: database.db")
print("=" * 50)