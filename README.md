# Employee Attendance and Salary Management System

A beginner-friendly Python project designed to track employee attendance, calculate overtime pay, determine overall attendance status, and generate a formatted salary summary report.

---

## 📋 Features

- **Employee Input Collection**: Accepts employee name, basic salary, total working days, present days, and overtime hours worked.
- **Attendance Calculation**: Computes attendance percentage based on total working days and present days.
- **Overtime Pay Calculation**: Calculates extra pay for overtime hours worked at a fixed rate of **Rs. 250/hour**.
- **Final Salary Calculation**: Computes total salary by adding basic salary and overtime earnings.
- **Attendance Threshold Evaluation**: Flags employees with less than **75% attendance** as `"Below Attendance Threshold"`, otherwise marks them as `"Attendance OK"`.
- **Formatted Summary Report**: Prints a clean summary report on the console.

---

## 🧮 Mathematical Formulas Used

| Calculation | Formula |
| :--- | :--- |
| **Attendance Percentage** | $\text{Attendance (\%)} = \left(\frac{\text{Present Days}}{\text{Total Working Days}}\right) \times 100$ |
| **Overtime Pay** | $\text{Overtime Pay} = \text{Overtime Hours} \times 250$ |
| **Final Salary** | $\text{Final Salary} = \text{Basic Salary} + \text{Overtime Pay}$ |

---

## 💻 Python Concepts Used

This project relies purely on standard Python built-ins without any third-party library dependencies:
- **Variables & Data Types**: Storing strings (`str`), floating point numbers (`float`), and integers (`int`).
- **User Input (`input()`)**: Collecting user input interactively via command line interface.
- **Arithmetic Operators**: `+`, `/`, `*` for calculating pay and attendance percentage.
- **Conditional Statements (`if / else`)**: Checking attendance thresholds and preventing division by zero.
- **Formatted Strings (f-strings)**: Formatting outputs with fixed decimal places and comma separators for currency.

---

## 🚀 How to Run the Project

### Prerequisites
Make sure you have **Python 3.x** installed on your system. You can check your Python version by running:
```bash
python --version
```

### Execution Steps
1. Open your terminal or command prompt in the project folder directory:
   ```bash
   cd path/to/Employee-Attendance-Salary
   ```
2. Run the main script:
   ```bash
   python main.py
   ```
3. Follow the on-screen prompts to enter employee details:
   - **Employee Name**: e.g., `John Doe`
   - **Basic Salary**: e.g., `50000`
   - **Total Working Days**: e.g., `22`
   - **Present Days**: e.g., `20`
   - **Overtime Hours Worked**: e.g., `10`

---

## 📊 Example Output

```text
==================================================
 EMPLOYEE ATTENDANCE AND SALARY MANAGEMENT SYSTEM 
==================================================

Please enter the employee details below:
Employee Name: John Doe
Basic Salary (Rs.): 50000
Total Working Days: 22
Present Days: 20
Overtime Hours Worked: 10

==================================================
               EMPLOYEE SUMMARY REPORT            
==================================================
Employee Name        : John Doe
Basic Salary         : Rs. 50,000.00
Attendance           : 90.91%
Overtime Hours       : 10.0 hrs
Overtime Pay         : Rs. 2,500.00
Final Salary         : Rs. 52,500.00
Attendance Status    : Attendance OK
==================================================
```
