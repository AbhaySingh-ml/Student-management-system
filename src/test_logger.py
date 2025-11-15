from file_handler import load_students, save_students

print("Testing logging system...")

students = load_students()
save_students(students)
