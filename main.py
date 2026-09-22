# Employee Attendance and Salary Management System
# A complete full-stack web application + CLI tool for tracking attendance, calculating overtime pay, and managing payroll summaries.

import sys
import os
import webbrowser
import subprocess

if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Add backend directory to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

def run_cli_calculator():
    """Runs the original interactive CLI calculator."""
    print("\n" + "=" * 50)
    print(" EMPLOYEE ATTENDANCE AND SALARY MANAGEMENT SYSTEM ")
    print("=" * 50)

    # 1. Take Employee Details as Input
    print("\nPlease enter the employee details below:")
    employee_name = input("Employee Name: ").strip() or "Anonymous Employee"
    basic_salary = float(input("Basic Salary (Rs.): ") or 0)
    total_working_days = int(input("Total Working Days: ") or 22)
    present_days = int(input("Present Days: ") or 0)
    overtime_hours = float(input("Overtime Hours Worked: ") or 0)

    # 2. Calculate Attendance Percentage
    if total_working_days > 0:
        attendance_percentage = (present_days / total_working_days) * 100
    else:
        attendance_percentage = 0.0

    # 3. Calculate Overtime Pay (fixed at Rs. 250 per hour)
    OVERTIME_RATE = 250.0
    overtime_pay = overtime_hours * OVERTIME_RATE

    # 4. Calculate Final Salary
    final_salary = basic_salary + overtime_pay

    # 5. Check Attendance Threshold (75%)
    ATTENDANCE_THRESHOLD = 75.0
    if attendance_percentage < ATTENDANCE_THRESHOLD:
        attendance_status = "Below Attendance Threshold"
    else:
        attendance_status = "Attendance OK"

    # 6. Generate Clear Summary Report
    print("\n" + "=" * 50)
    print("               EMPLOYEE SUMMARY REPORT            ")
    print("=" * 50)
    print(f"Employee Name        : {employee_name}")
    print(f"Basic Salary         : Rs. {basic_salary:,.2f}")
    print(f"Attendance           : {attendance_percentage:.2f}%")
    print(f"Overtime Hours       : {overtime_hours:.1f} hrs")
    print(f"Overtime Pay         : Rs. {overtime_pay:,.2f}")
    print(f"Final Salary         : Rs. {final_salary:,.2f}")
    print(f"Attendance Status    : {attendance_status}")
    print("=" * 50)

def start_web_server():
    """Launches the Flask Full-Stack Web App Server and opens default web browser."""
    print("\n" + "=" * 60)
    print(" 🚀 LAUNCHING FULL-STACK WEB MANAGEMENT SYSTEM ")
    print("=" * 60)
    print("• Backend API: http://127.0.0.1:5000/api")
    print("• Frontend Web Dashboard: http://127.0.0.1:5000")
    print("=" * 60 + "\n")

    # Automatically open browser after 1 second
    try:
        webbrowser.open("http://127.0.0.1:5000")
    except Exception:
        pass

    from app import app
    app.run(host="0.0.0.0", port=5000, debug=False)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--web":
        start_web_server()
        return

    print("=" * 60)
    print(" EMPLOYEE ATTENDANCE & SALARY MANAGEMENT SYSTEM ")
    print("=" * 60)
    print("Choose Mode:")
    print("1) Launch Full-Stack Web Application (Frontend + REST API Backend)")
    print("2) Run CLI Calculator")
    print("3) Exit")
    print("-" * 60)

    choice = input("Enter option (1, 2, or 3) [Default: 1]: ").strip()

    if choice == "2":
        run_cli_calculator()
    elif choice == "3":
        print("Goodbye!")
        sys.exit(0)
    else:
        start_web_server()

if __name__ == "__main__":
    main()
