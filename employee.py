import sqlite3
from datetime import datetime

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('employee_management.db')
cursor = conn.cursor()

# Create the employees table
cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    position TEXT NOT NULL,
    department TEXT NOT NULL,
    salary REAL NOT NULL,
    hire_date TEXT NOT NULL
)
''')

conn.commit()

def add_employee(name, position, department, salary):
    hire_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
    INSERT INTO employees (name, position, department, salary, hire_date)
    VALUES (?, ?, ?, ?, ?)
    ''', (name, position, department, salary, hire_date))
    conn.commit()
    print(f"Employee {name} added successfully.")

def get_employee(emp_id):
    cursor.execute('''
    SELECT * FROM employees WHERE id = ?
    ''', (emp_id,))
    employee = cursor.fetchone()
    if employee:
        print(f"ID: {employee[0]}, Name: {employee[1]}, Position: {employee[2]}, Department: {employee[3]}, Salary: {employee[4]}, Hire Date: {employee[5]}")
    else:
        print("Employee not found.")

def update_employee(emp_id, name=None, position=None, department=None, salary=None):
    employee = cursor.execute('SELECT * FROM employees WHERE id = ?', (emp_id,)).fetchone()
    if not employee:
        print("Employee not found.")
        return

    updated_name = name if name else employee[1]
    updated_position = position if position else employee[2]
    updated_department = department if department else employee[3]
    updated_salary = salary if salary else employee[4]

    cursor.execute('''
    UPDATE employees
    SET name = ?, position = ?, department = ?, salary = ?
    WHERE id = ?
    ''', (updated_name, updated_position, updated_department, updated_salary, emp_id))
    conn.commit()
    print(f"Employee {emp_id} updated successfully.")

def delete_employee(emp_id):
    cursor.execute('''
    DELETE FROM employees WHERE id = ?
    ''', (emp_id,))
    conn.commit()
    print(f"Employee {emp_id} deleted successfully.")

def list_employees():
    cursor.execute('SELECT * FROM employees')
    employees = cursor.fetchall()
    if employees:
        for emp in employees:
            print(f"ID: {emp[0]}, Name: {emp[1]}, Position: {emp[2]}, Department: {emp[3]}, Salary: {emp[4]}, Hire Date: {emp[5]}")
    else:
        print("No employees found.")

def main():
    while True:
        print("\nEmployee Management System")
        print("1. Add Employee")
        print("2. Get Employee")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. List Employees")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter name: ")
            position = input("Enter position: ")
            department = input("Enter department: ")
            salary = float(input("Enter salary: "))
            add_employee(name, position, department, salary)
        elif choice == '2':
            emp_id = int(input("Enter employee ID: "))
            get_employee(emp_id)
        elif choice == '3':
            emp_id = int(input("Enter employee ID: "))
            name = input("Enter name (leave blank to keep current): ")
            position = input("Enter position (leave blank to keep current): ")
            department = input("Enter department (leave blank to keep current): ")
            salary = input("Enter salary (leave blank to keep current): ")
            salary = float(salary) if salary else None
            update_employee(emp_id, name, position, department, salary)
        elif choice == '4':
            emp_id = int(input("Enter employee ID: "))
            delete_employee(emp_id)
        elif choice == '5':
            list_employees()
        elif choice == '6':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

# Close the connection when the script exits
conn.close()
