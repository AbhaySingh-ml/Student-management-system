from file_handler import load_data, save_data

def test_file_handler():
    students = load_data()
    print("Before:", students)

    # Add a test record
    test_student = {"name": "Abhay", "roll_no": 1, "marks": 90, "grade": "A"}
    students.append(test_student)

    save_data(students)
    print("Saved successfully!")

    # Reload and print again
    reloaded = load_data()
    print("After reload:", reloaded)

if __name__ == "__main__":
    test_file_handler()
