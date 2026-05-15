"""
Project: Student Grade Tracker
Pre-Work Section C — Python Fundamentals
Estimated time: 45-60 minutes

Objective: Build a data processing script that reads student grades from
a CSV, calculates averages, assigns letter grades, and writes a summary report.

Your job: implement all the functions marked with # TODO.
Do NOT modify the function signatures or the main() function.
"""

import csv


# ============================================================
# FUNCTION 1: Load data from CSV
# ============================================================

def load_students(filepath: str) -> list[dict]:
    """
    Read student data from a CSV file.

    Each row becomes a dictionary. The CSV has columns:
    student_name, math, science, english, history

    Some cells may be empty strings (missing grades) — that's expected.

    Args:
        filepath: Path to the CSV file.

    Returns:
        A list of dicts, one per student.
        Example: [{"student_name": "Alice", "math": "92", ...}, ...]

    Raises:
        FileNotFoundError: if the CSV file doesn't exist.
    """
    try:
        with open(filepath) as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        return f"Error: file not found: {filepath}"


# ============================================================
# FUNCTION 2: Calculate average, handling missing values
# ============================================================

def calculate_average(grades: list) -> float | None:
    """
    Calculate the average of a list of grade values.

    Grade values may be strings (from the CSV), empty strings, or numbers.
    Ignore any value that can't be converted to a float.

    Args:
        grades: A list of values (e.g., ["92", "88", "", "79"]).

    Returns:
        The average as a float, rounded to 1 decimal place.
        Returns None if there are no valid grades.
    """
    valid_grades = []
    for value in grades:
        try:
            grade = float(value)
        except (ValueError, TypeError):
            continue
        valid_grades.append(grade)

    if not valid_grades:
        return None

    average = sum(valid_grades) / len(valid_grades)
    return round(average, 1)


# ============================================================
# FUNCTION 3: Assign letter grade
# ============================================================

def get_letter_grade(average: float | None) -> str:
    """
    Convert a numeric average to a letter grade.

    Scale:
        90+  → "A"
        80-89 → "B"
        70-79 → "C"
        60-69 → "D"
        < 60  → "F"
        None  → "N/A" (no grades available)

    Args:
        average: The numeric average, or None.

    Returns:
        The letter grade as a string.
    """
    if average is None:
        return "N/A"
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"


# ============================================================
# FUNCTION 4: Generate summary report
# ============================================================

def generate_report(students: list[dict]) -> dict:
    """
    Generate a class summary report.

    Args:
        students: The list of student dicts from load_students().

    Returns:
        A dict with these keys:
            "total_students":   int — how many students
            "class_average":    float — average of all valid averages
            "highest_average":  float — the best average
            "lowest_average":   float — the lowest average
            "grade_distribution": dict — {"A": 3, "B": 5, ...}
            "students":         list of dicts, each with:
                                  name, average, grade
    """
    student_summaries = []
    grade_distribution = {}
    averages = []

    for student in students:
        grades = [
            student.get("math", ""),
            student.get("science", ""),
            student.get("english", ""),
            student.get("history", ""),
        ]
        average = calculate_average(grades)
        grade = get_letter_grade(average)

        student_summaries.append({
            "name": student.get("student_name", ""),
            "average": average,
            "grade": grade,
        })

        grade_distribution[grade] = grade_distribution.get(grade, 0) + 1
        if average is not None:
            averages.append(average)

    class_average = round(sum(averages) / len(averages), 1) if averages else None
    highest_average = max(averages) if averages else None
    lowest_average = min(averages) if averages else None

    return {
        "total_students": len(students),
        "class_average": class_average,
        "highest_average": highest_average,
        "lowest_average": lowest_average,
        "grade_distribution": grade_distribution,
        "students": student_summaries,
    }


# ============================================================
# FUNCTION 5: Write report to a file
# ============================================================

def write_report(report: dict, filepath: str) -> None:
    """
    Write the summary report to a text file.

    Format example:
        ===========================
        STUDENT GRADE REPORT
        ===========================
        Total students: 15
        Class average:  81.3
        Highest average: 95.0
        Lowest average:  55.0

        Grade Distribution:
          A: 5
          B: 4
          ...

        Individual Results:
          Alice Johnson    Avg: 91.5  Grade: A
          ...

    Args:
        report:   The dict returned by generate_report().
        filepath: Path to write the report file.
    """
    with open(filepath, "w") as f:
        header_line = "=" * 45
        title = "STUDENT GRADE REPORT".center(len(header_line))
        f.write(f"{header_line}\n")
        f.write(f"{title}\n")
        f.write(f"{header_line}\n")
        f.write(f"Total students: {report['total_students']}\n")
        f.write(f"Class average:  {report['class_average']}\n")
        f.write(f"Highest average: {report['highest_average']}\n")
        f.write(f"Lowest average:  {report['lowest_average']}\n\n")

        f.write("Grade Distribution:\n")
        for grade, count in sorted(report["grade_distribution"].items()):
            f.write(f"{grade}: {count}\n")

        f.write("\nIndividual Results:\n")
        for student in report["students"]:
            average_text = "N/A" if student["average"] is None else f"{student['average']:.1f}"
            f.write(f"{student['name']:<20} Avg: {average_text}  Grade: {student['grade']}\n")


# ============================================================
# MAIN — do not modify
# ============================================================

def main():
    print("Loading student data...")
    students = load_students("data/students.csv")
    print(f"Loaded {len(students)} students.")

    print("Generating report...")
    report = generate_report(students)

    print("\n--- Summary ---")
    print(f"Total students:   {report['total_students']}")
    print(f"Class average:    {report['class_average']}")
    print(f"Highest average:  {report['highest_average']}")
    print(f"Lowest average:   {report['lowest_average']}")

    print("\nGrade Distribution:")
    for grade, count in sorted(report["grade_distribution"].items()):
        print(f"  {grade}: {count}")

    print("\nTop 5 students:")
    sorted_students = sorted(
        [s for s in report["students"] if s["average"] is not None],
        key=lambda s: s["average"],
        reverse=True
    )
    for s in sorted_students[:5]:
        print(f"  {s['name']:<20} {s['average']:.1f}  ({s['grade']})")

    write_report(report, "grade_report.txt")
    print("\nReport written to grade_report.txt")


if __name__ == "__main__":
    main()