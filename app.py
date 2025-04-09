import streamlit as st
import mysql.connector

# -------------------------------
# 🛠️ Database Connection
# -------------------------------
try:
    con = mysql.connector.connect(
        host="database-1.cfwoukks6awx.eu-north-1.rds.amazonaws.com",
        user="admin",
        password="sharankk123",
        database="emp"
    )
    cursor = con.cursor()
except mysql.connector.Error as e:
    st.error(f"❌ Could not connect to the database: {e}")
    st.stop()

# -------------------------------
# 🔍 Helper Functions
# -------------------------------
def check_employee(employee_id):
    cursor.execute('SELECT * FROM employees WHERE id=%s', (employee_id,))
    return cursor.fetchone() is not None

def add_employee(emp_id, name, post, salary):
    if check_employee(emp_id):
        return "⚠️ Employee already exists!"
    try:
        cursor.execute(
            'INSERT INTO employees (id, name, post, salary) VALUES (%s, %s, %s, %s)',
            (emp_id, name, post, salary)
        )
        con.commit()
        return "✅ Employee added successfully!"
    except mysql.connector.Error as err:
        con.rollback()
        return f"❌ Database error: {err}"

def remove_employee(emp_id):
    if not check_employee(emp_id):
        return "⚠️ Employee does not exist!"
    try:
        cursor.execute('DELETE FROM employees WHERE id=%s', (emp_id,))
        con.commit()
        return "🗑️ Employee removed successfully!"
    except mysql.connector.Error as err:
        con.rollback()
        return f"❌ Database error: {err}"

def promote_employee(emp_id, increase):
    if not check_employee(emp_id):
        return "⚠️ Employee does not exist!"
    try:
        cursor.execute('SELECT salary FROM employees WHERE id=%s', (emp_id,))
        current_salary = cursor.fetchone()[0]
        new_salary = current_salary + increase
        cursor.execute('UPDATE employees SET salary=%s WHERE id=%s', (new_salary, emp_id))
        con.commit()
        return f"📈 Salary updated to ₹{new_salary:,.2f}"
    except mysql.connector.Error as err:
        con.rollback()
        return f"❌ Database error: {err}"

def get_all_employees():
    cursor.execute('SELECT * FROM employees')
    return cursor.fetchall()

# -------------------------------
# 🌐 Streamlit UI
# -------------------------------
st.set_page_config(page_title="Employee Management System", layout="centered")
st.title("👨‍💼 Employee Management System")

menu = ["Add Employee", "Remove Employee", "Promote Employee", "View Employees"]
choice = st.sidebar.radio("📋 Menu", menu)

# ➕ Add Employee
if choice == "Add Employee":
    st.subheader("➕ Add New Employee")
    emp_id = st.number_input("Employee ID", min_value=1, step=1)
    name = st.text_input("Employee Name")
    post = st.text_input("Post")
    salary = st.number_input("Salary", min_value=0.0, step=100.0)
    if st.button("Add"):
        if name and post:
            result = add_employee(emp_id, name, post, salary)
            st.success(result)
        else:
            st.warning("Please fill all fields.")

# 🗑️ Remove Employee
elif choice == "Remove Employee":
    st.subheader("🗑️ Remove Employee")
    emp_id = st.number_input("Employee ID", min_value=1, step=1)
    if st.button("Remove"):
        result = remove_employee(emp_id)
        st.warning(result)

# 📈 Promote Employee
elif choice == "Promote Employee":
    st.subheader("📈 Promote Employee")
    emp_id = st.number_input("Employee ID", min_value=1, step=1)
    increment = st.number_input("Increment Salary By", min_value=0.0, step=100.0)
    if st.button("Promote"):
        result = promote_employee(emp_id, increment)
        st.success(result)

# 📋 View Employees
elif choice == "View Employees":
    st.subheader("📋 All Employees")
    employees = get_all_employees()
    if employees:
        st.table(employees)
    else:
        st.info("No employees found.")
