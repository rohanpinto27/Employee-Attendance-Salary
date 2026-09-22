import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "employees.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            basic_salary REAL NOT NULL,
            total_working_days INTEGER NOT NULL,
            present_days INTEGER NOT NULL,
            overtime_hours REAL NOT NULL DEFAULT 0.0,
            overtime_rate REAL NOT NULL DEFAULT 250.0,
            attendance_percentage REAL NOT NULL,
            overtime_pay REAL NOT NULL,
            final_salary REAL NOT NULL,
            attendance_status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    
    # Seed initial sample data if table is empty
    cursor.execute('SELECT COUNT(*) FROM employees')
    count = cursor.fetchone()[0]
    if count == 0:
        sample_employees = [
            ("John Doe", 50000.0, 22, 20, 10.0, 250.0),
            ("Jane Smith", 65000.0, 22, 22, 5.0, 250.0),
            ("Robert Johnson", 42000.0, 22, 14, 0.0, 250.0),
            ("Emily Davis", 58000.0, 22, 21, 12.5, 250.0),
            ("Michael Brown", 48000.0, 22, 15, 2.0, 250.0)
        ]
        for name, basic_salary, total_days, present_days, ot_hours, ot_rate in sample_employees:
            att_pct = (present_days / total_days * 100) if total_days > 0 else 0.0
            ot_pay = ot_hours * ot_rate
            final_sal = basic_salary + ot_pay
            status = "Below Attendance Threshold" if att_pct < 75.0 else "Attendance OK"
            
            cursor.execute('''
                INSERT INTO employees (
                    name, basic_salary, total_working_days, present_days, 
                    overtime_hours, overtime_rate, attendance_percentage, 
                    overtime_pay, final_salary, attendance_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, basic_salary, total_days, present_days, ot_hours, ot_rate, att_pct, ot_pay, final_sal, status))
        conn.commit()
        
    conn.close()
