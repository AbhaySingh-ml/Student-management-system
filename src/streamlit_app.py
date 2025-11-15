import streamlit as st
from student_manager import StudentManager
from utils import calculate_grade, validate_roll_no
from file_handler import save_students

# -------------------- PAGE SETUP --------------------
st.set_page_config(
    page_title="Student Management System",
    layout="centered",
    page_icon="🎓"
)

st.title("🎓 Student Record Management System")
st.markdown("---")

# Initialize the manager (loads from JSON)
manager = StudentManager()

# -------------------- SIDEBAR MENU --------------------
menu = [
    "🏠 Home",
    "➕ Add Student",
    "📚 View Students",
    "✏️ Update Student",
    "❌ Delete Student",
    "📊 Sort Students"
]
choice = st.sidebar.selectbox("📋 Choose an action", menu)

# -------------------- HOME PAGE --------------------
if choice == "🏠 Home":
    st.subheader("Welcome to the Student Management System")
    st.markdown("""
    This app allows you to manage student records easily:
    - ➕ Add new students  
    - 👀 View all records  
    - ✏️ Update marks or names  
    - ❌ Delete records  
    - 📊 Sort by name or marks  
    ---
    **Data is stored persistently in JSON** and all actions are logged automatically.
    """)

# -------------------- ADD STUDENT --------------------
elif choice == "➕ Add Student":
    st.subheader("➕ Add New Student")

    with st.form("add_form"):
        name = st.text_input("Enter Name")
        roll_no = st.number_input("Enter Roll Number", min_value=1, step=1)
        marks = st.number_input("Enter Marks", min_value=0, max_value=100, step=1)
        submitted = st.form_submit_button("Add Student")

        if submitted:
            if not name.strip():
                st.warning("Name cannot be empty.")
            elif not validate_roll_no(roll_no, manager.students):
                st.warning("⚠️ Roll number already exists!")
            else:
                student = {
                    "name": name.strip(),
                    "roll_no": roll_no,
                    "marks": marks,
                    "grade": calculate_grade(marks)
                }
                manager.students.append(student)
                save_students(manager.students)
                st.success(f"✅ Student '{name}' added successfully!")

# -------------------- VIEW STUDENTS --------------------
elif choice == "📚 View Students":
    st.subheader("📚 All Student Records")

    if not manager.students:
        st.info("No students found.")
    else:
        st.dataframe(manager.students, use_container_width=True)

# -------------------- UPDATE STUDENT --------------------
elif choice == "✏️ Update Student":
    st.subheader("✏️ Update Student Details")

    roll_no = st.number_input("Enter Roll Number to Update", min_value=1, step=1)
    student = next((s for s in manager.students if s["roll_no"] == roll_no), None)

    if student:
        st.write(f"Editing Record for: **{student['name']}**")
        new_name = st.text_input("New Name", value=student["name"])
        new_marks = st.number_input("New Marks", value=student["marks"], min_value=0, max_value=100, step=1)

        if st.button("Update"):
            student["name"] = new_name.strip()
            student["marks"] = new_marks
            student["grade"] = calculate_grade(new_marks)
            save_students(manager.students)
            st.success("✅ Student record updated successfully!")
    else:
        st.info("Enter a valid roll number to edit.")

# -------------------- DELETE STUDENT --------------------
elif choice == "❌ Delete Student":
    st.subheader("❌ Delete Student Record")

    roll_no = st.number_input("Enter Roll Number to Delete", min_value=1, step=1)
    student = next((s for s in manager.students if s["roll_no"] == roll_no), None)

    if student:
        st.warning(f"Are you sure you want to delete '{student['name']}'?")
        if st.button("Confirm Delete"):
            manager.students.remove(student)
            save_students(manager.students)
            st.success(f"✅ Deleted student '{student['name']}' successfully!")
    else:
        st.info("Enter a valid roll number to delete.")

# -------------------- SORT STUDENTS --------------------
elif choice == "📊 Sort Students":
    st.subheader("📊 Sort Students")

    if not manager.students:
        st.warning("⚠️ No students to sort.")
    else:
        sort_type = st.selectbox("Sort by:", ["Name (A-Z)", "Marks (High to Low)"])
        if sort_type == "Name (A-Z)":
            sorted_students = sorted(manager.students, key=lambda s: s["name"].lower())
        else:
            sorted_students = sorted(manager.students, key=lambda s: s["marks"], reverse=True)
        st.dataframe(sorted_students, use_container_width=True)

