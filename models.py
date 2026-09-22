def calculate_metrics(basic_salary, total_working_days, present_days, overtime_hours, overtime_rate=250.0):
    """
    Core business logic calculation function matching project formulas:
    - Attendance (%) = (Present Days / Total Working Days) * 100
    - Overtime Pay = Overtime Hours * Overtime Rate (default 250/hr)
    - Final Salary = Basic Salary + Overtime Pay
    - Attendance Threshold = 75% ('Attendance OK' vs 'Below Attendance Threshold')
    """
    total_working_days = max(0, int(total_working_days))
    present_days = max(0, min(total_working_days, int(present_days)))
    basic_salary = max(0.0, float(basic_salary))
    overtime_hours = max(0.0, float(overtime_hours))
    overtime_rate = max(0.0, float(overtime_rate))

    if total_working_days > 0:
        attendance_percentage = round((present_days / total_working_days) * 100, 2)
    else:
        attendance_percentage = 0.0

    overtime_pay = round(overtime_hours * overtime_rate, 2)
    final_salary = round(basic_salary + overtime_pay, 2)

    ATTENDANCE_THRESHOLD = 75.0
    if attendance_percentage < ATTENDANCE_THRESHOLD:
        attendance_status = "Below Attendance Threshold"
    else:
        attendance_status = "Attendance OK"

    return {
        "basic_salary": basic_salary,
        "total_working_days": total_working_days,
        "present_days": present_days,
        "overtime_hours": overtime_hours,
        "overtime_rate": overtime_rate,
        "attendance_percentage": attendance_percentage,
        "overtime_pay": overtime_pay,
        "final_salary": final_salary,
        "attendance_status": attendance_status
    }

def employee_row_to_dict(row):
    """Converts SQLite Row to JSON serializable Python dict."""
    if not row:
        return None
    return {
        "id": row["id"],
        "name": row["name"],
        "basic_salary": row["basic_salary"],
        "total_working_days": row["total_working_days"],
        "present_days": row["present_days"],
        "overtime_hours": row["overtime_hours"],
        "overtime_rate": row["overtime_rate"],
        "attendance_percentage": row["attendance_percentage"],
        "overtime_pay": row["overtime_pay"],
        "final_salary": row["final_salary"],
        "attendance_status": row["attendance_status"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"]
    }
