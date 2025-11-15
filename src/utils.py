def calculate_grade(marks):
    """Return grade based on marks."""
    pass

def validate_roll_no(roll_no, students):
    """Ensure roll number is unique."""
    pass
def calculate_grade(marks):
    """Return grade based on marks."""
    if marks >= 90:
        return "A"
    elif marks >= 75:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 40:
        return "D"
    else:
        return "F"
def validate_roll_no(roll_no, students):
    """Ensure roll number is unique."""
    for student in students:
        if student.get("roll_no") == roll_no:
            return False
    return True