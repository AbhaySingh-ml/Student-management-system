from logger_setup import get_logger
from file_handler import load_students, save_students
from utils import calculate_grade
from utils import validate_roll_no 
import json

logger = get_logger(__name__)

class StudentManager:
    def __init__(self):
        """Initialize manager and load students from file."""
        self.students = load_students()
        logger.info(f"Loaded {len(self.students)} student(s) from file.")

    def add_student(self):
        """Add a new student record."""
        user_input = input(
            'Enter student details in JSON format (e.g., {"name": "Abhay", "roll_no": 1, "marks": 85}): '
        )

        try:
            student_data = json.loads(user_input)
            # Validate required keys
            required_keys = ["name", "roll_no", "marks"]
            for key in required_keys:
                if key not in student_data:
                    print(f"❌ Missing key: {key}. Please include all required fields.")
                    logger.warning(f"Missing key while adding student: {key}")
                    return

            # Ensure roll_no is unique
            # if any(s["roll_no"] == student_data["roll_no"] for s in self.students):
            #     print("⚠️ Roll number already exists. Please use a unique roll number.")
            #     logger.warning(f"Duplicate roll_no {student_data['roll_no']} attempted.")
            #     return
            
            if not validate_roll_no(student_data["roll_no"], self.students):
                print("⚠️ Roll number already exists. Please use a unique roll number.")
                logger.warning(f"Duplicate roll_no {student_data['roll_no']} attempted.")
                return

            
            
            # #Ensure that name is also unique
            # if any(s['Name']== student_data["Name"]for s in self.students):
            #     print("⚠️ Name is already exist try another name")
            #     logger.warning(f"Duplicate name {student_data['name']} attempted.")

            # Auto-calculate grade
            student_data["grade"] = calculate_grade(student_data["marks"])

            # Add student and save
            self.students.append(student_data)
            save_students(self.students)
            logger.info(f"Added student: {student_data['name']}")
            print("✅ Student added and saved successfully!")

        except json.JSONDecodeError:
            print("❌ Invalid JSON format. Please try again.")
            logger.error("Error while adding student - invalid JSON")

    def view_students(self):
        """Display all student records."""
        if not self.students:
            print("⚠️ No students found.")
            return

        print("\n📚 Student Records:")
        print("-" * 60)
        for s in self.students:
            print(
                f"Name: {s['name']}, Roll No: {s['roll_no']}, Marks: {s['marks']}, Grade: {s.get('grade', 'N/A')}"
            )
        print("-" * 60)

    def update_student(self):
        """Update an existing student's details by roll number."""
        try:
            roll_no = int(input("Enter the roll number of the student to update: "))
        except ValueError:
            print("❌ Invalid input. Please enter a valid roll number.")
            return

        for student in self.students:
            if student["roll_no"] == roll_no:
                print(f"Found student: {student['name']} (Marks: {student['marks']})")
                field = input("What do you want to update? (name/marks): ").strip().lower()

                if field == "name":
                    new_name = input("Enter new name: ").strip()
                    student["name"] = new_name
                    print("✅ Name updated successfully!")

                elif field == "marks":
                    try:
                        old_marks = student["marks"]
                        new_marks = int(input("Enter new marks: "))
                        student["marks"] = new_marks
                        student["grade"] = calculate_grade(new_marks)
                        print("✅ Marks updated successfully!")
                        logger.info(f"Updated marks for {student['name']} from {old_marks} to {new_marks}")
                    except ValueError:
                        print("❌ Invalid marks. Must be a number.")
                        return
                else:
                    print("⚠️ Invalid choice. You can only update 'name' or 'marks'.")
                    return

                # Save updates
                save_students(self.students)
                logger.info(f"Updated student record for roll_no {roll_no}")
                return

        print("⚠️ No student found with that roll number.")
        logger.warning(f"Attempted to update non-existing student with roll_no {roll_no}")

    def delete_student(self):
        """Delete a student record by roll number."""
        try:
            roll_no = int(input("Enter the roll number of the student to delete: "))
        except ValueError:
            print("❌ Invalid input. Please enter a valid roll number.")
            return

        for student in self.students:
            if student["roll_no"] == roll_no:
                confirm = input(
                    f"Are you sure you want to delete {student['name']}? (y/n): "
                ).strip().lower()
                if confirm == "y":
                    self.students.remove(student)
                    save_students(self.students)
                    print("✅ Student deleted successfully!")
                    logger.info(f"Deleted student record for roll_no {roll_no}")
                else:
                    print("❎ Deletion cancelled.")
                return  # Exit after processing

        print("⚠️ No student found with that roll number.")
        logger.warning(f"Attempted to delete non-existing student with roll_no {roll_no}")

    def sort_students(self):
        """Sort students by marks or name."""
        if not self.students:
            print("⚠️ No students to sort.")
            return

        print("Sort by:\n1. Name\n2. Marks")
        choice = input("Enter your choice (1/2): ").strip()

        if choice == "1":
            sorted_students = sorted(self.students, key=lambda s: s["name"].lower())
            print("\n📚 Students sorted by name:")
        elif choice == "2":
            sorted_students = sorted(
                self.students, key=lambda s: s["marks"], reverse=True
            )
            print("\n📊 Students sorted by marks (highest first):")
        else:
            print("⚠️ Invalid choice.")
            return

        print("-" * 60)
        for s in sorted_students:
            print(
                f"Name: {s['name']}, Roll No: {s['roll_no']}, Marks: {s['marks']}, Grade: {s.get('grade', 'N/A')}"
            )
        print("-" * 60)

