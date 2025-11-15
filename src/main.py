from student_manager import StudentManager


def main():
    """Main menu for the Student Record Management System."""
    manager = StudentManager()

    while True:
        print("\n===== 🎓 Student Record Management System =====")
        print("1. ➕ Add Student")
        print("2. 👁 View All Students")
        print("3. ✏ Update Student")
        print("4. 🗑 Delete Student")
        print("5. 📊 Sort Students")
        print("6. 🚪 Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            manager.add_student()

        elif choice == '2':
            manager.view_students()

        elif choice == '3':
            manager.update_student()

        elif choice == '4':
            manager.delete_student()

        elif choice == '5':
            manager.sort_students()

        elif choice == '6':
            print("\n👋 Exiting... Goodbye!")
            break

        else:
            print("⚠️ Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Program interrupted by user. Exiting safely...")

