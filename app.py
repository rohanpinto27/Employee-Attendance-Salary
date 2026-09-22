import sys
import os
import io
import csv

if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS

from database import init_db, get_db_connection
from models import calculate_metrics, employee_row_to_dict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app)

# Initialize Database tables and sample seed data
init_db()

@app.route("/")
def serve_index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/css/<path:filename>")
def serve_css(filename):
    return send_from_directory(os.path.join(FRONTEND_DIR, "css"), filename)

@app.route("/js/<path:filename>")
def serve_js(filename):
    return send_from_directory(os.path.join(FRONTEND_DIR, "js"), filename)

# --- REST API ENDPOINTS ---

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "Employee Attendance & Salary Management System API",
        "version": "1.0.0"
    })

@app.route("/api/calculate", methods=["POST"])
def calculate_preview():
    data = request.get_json() or {}
    try:
        basic_salary = float(data.get("basic_salary", 0))
        total_days = int(data.get("total_working_days", 0))
        present_days = int(data.get("present_days", 0))
        overtime_hours = float(data.get("overtime_hours", 0))
        overtime_rate = float(data.get("overtime_rate", 250.0))

        result = calculate_metrics(basic_salary, total_days, present_days, overtime_hours, overtime_rate)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/api/employees", methods=["GET"])
def get_employees():
    search_query = request.args.get("search", "").strip()
    status_filter = request.args.get("status", "").strip()

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM employees WHERE 1=1"
    params = []

    if search_query:
        query += " AND name LIKE ?"
        params.append(f"%{search_query}%")

    if status_filter:
        query += " AND attendance_status = ?"
        params.append(status_filter)

    query += " ORDER BY id DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    employees = [employee_row_to_dict(r) for r in rows]
    return jsonify({"success": True, "count": len(employees), "employees": employees})

@app.route("/api/employees/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"success": False, "error": "Employee not found"}), 404

    return jsonify({"success": True, "employee": employee_row_to_dict(row)})

@app.route("/api/employees", methods=["POST"])
def create_employee():
    data = request.get_json() or {}
    name = data.get("name", "").strip()

    if not name:
        return jsonify({"success": False, "error": "Employee name is required"}), 400

    try:
        basic_salary = float(data.get("basic_salary", 0))
        total_working_days = int(data.get("total_working_days", 0))
        present_days = int(data.get("present_days", 0))
        overtime_hours = float(data.get("overtime_hours", 0))
        overtime_rate = float(data.get("overtime_rate", 250.0))
    except (ValueError, TypeError):
        return jsonify({"success": False, "error": "Invalid numerical parameters"}), 400

    metrics = calculate_metrics(basic_salary, total_working_days, present_days, overtime_hours, overtime_rate)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO employees (
            name, basic_salary, total_working_days, present_days, 
            overtime_hours, overtime_rate, attendance_percentage, 
            overtime_pay, final_salary, attendance_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        name, metrics["basic_salary"], metrics["total_working_days"], metrics["present_days"],
        metrics["overtime_hours"], metrics["overtime_rate"], metrics["attendance_percentage"],
        metrics["overtime_pay"], metrics["final_salary"], metrics["attendance_status"]
    ))
    conn.commit()
    new_id = cursor.lastrowid
    
    cursor.execute("SELECT * FROM employees WHERE id = ?", (new_id,))
    new_row = cursor.fetchone()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Employee created successfully",
        "employee": employee_row_to_dict(new_row)
    }), 201

@app.route("/api/employees/<int:employee_id>", methods=["PUT"])
def update_employee(employee_id):
    data = request.get_json() or {}
    name = data.get("name", "").strip()

    if not name:
        return jsonify({"success": False, "error": "Employee name is required"}), 400

    try:
        basic_salary = float(data.get("basic_salary", 0))
        total_working_days = int(data.get("total_working_days", 0))
        present_days = int(data.get("present_days", 0))
        overtime_hours = float(data.get("overtime_hours", 0))
        overtime_rate = float(data.get("overtime_rate", 250.0))
    except (ValueError, TypeError):
        return jsonify({"success": False, "error": "Invalid numerical parameters"}), 400

    metrics = calculate_metrics(basic_salary, total_working_days, present_days, overtime_hours, overtime_rate)

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"success": False, "error": "Employee not found"}), 404

    cursor.execute('''
        UPDATE employees SET
            name = ?,
            basic_salary = ?,
            total_working_days = ?,
            present_days = ?,
            overtime_hours = ?,
            overtime_rate = ?,
            attendance_percentage = ?,
            overtime_pay = ?,
            final_salary = ?,
            attendance_status = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (
        name, metrics["basic_salary"], metrics["total_working_days"], metrics["present_days"],
        metrics["overtime_hours"], metrics["overtime_rate"], metrics["attendance_percentage"],
        metrics["overtime_pay"], metrics["final_salary"], metrics["attendance_status"],
        employee_id
    ))
    conn.commit()

    cursor.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
    updated_row = cursor.fetchone()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Employee updated successfully",
        "employee": employee_row_to_dict(updated_row)
    })

@app.route("/api/employees/<int:employee_id>", methods=["DELETE"])
def delete_employee(employee_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"success": False, "error": "Employee not found"}), 404

    cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": f"Employee #{employee_id} deleted successfully"})

@app.route("/api/summary", methods=["GET"])
def get_summary():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            COUNT(*) as total_employees,
            COALESCE(SUM(basic_salary), 0) as total_basic_salary,
            COALESCE(SUM(overtime_pay), 0) as total_overtime_pay,
            COALESCE(SUM(final_salary), 0) as total_payroll,
            COALESCE(AVG(attendance_percentage), 0) as avg_attendance,
            SUM(CASE WHEN attendance_percentage < 75.0 THEN 1 ELSE 0 END) as low_attendance_count,
            SUM(CASE WHEN attendance_percentage >= 75.0 THEN 1 ELSE 0 END) as ok_attendance_count
        FROM employees
    ''')
    row = cursor.fetchone()
    conn.close()

    summary = {
        "total_employees": row["total_employees"],
        "total_basic_salary": round(row["total_basic_salary"], 2),
        "total_overtime_pay": round(row["total_overtime_pay"], 2),
        "total_payroll": round(row["total_payroll"], 2),
        "avg_attendance": round(row["avg_attendance"], 2),
        "low_attendance_count": row["low_attendance_count"] or 0,
        "ok_attendance_count": row["ok_attendance_count"] or 0
    }

    return jsonify({"success": True, "summary": summary})

@app.route("/api/export/csv", methods=["GET"])
def export_csv():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "ID", "Employee Name", "Basic Salary (Rs)", "Total Working Days",
        "Present Days", "Attendance (%)", "Overtime Hours", "Overtime Pay (Rs)",
        "Final Salary (Rs)", "Attendance Status"
    ])

    for r in rows:
        writer.writerow([
            r["id"], r["name"], f"{r['basic_salary']:.2f}", r["total_working_days"],
            r["present_days"], f"{r['attendance_percentage']:.2f}%",
            f"{r['overtime_hours']:.1f}", f"{r['overtime_pay']:.2f}",
            f"{r['final_salary']:.2f}", r["attendance_status"]
        ])

    csv_data = output.getvalue()
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=Employee_Salary_Report.csv"}
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Starting Employee Attendance & Salary Management Web Server on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
