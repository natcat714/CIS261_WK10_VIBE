"""Student Grade Calculator."""

from dataclasses import dataclass
from pathlib import Path


FILE_NAME = Path("student_grades.txt")

class Intro:
	def __init__(self):
		print("=" * 60)
		print("WELCOME TO STUDENT GRADE CALCULATOR")
		print("=" * 60)
		
@dataclass
class Student:
	"""Store one student's scores and calculated results."""

	name: str
	student_id: str
	test1: float
	test2: float
	test3: float
	average: float = 0.0
	grade: str = "F"

	def __post_init__(self):
		self.calculate_grade()

	def calculate_grade(self):
		self.average = (self.test1 + self.test2 + self.test3) / 3
		if self.average >= 90:
			self.grade = "A"
		elif self.average >= 80:
			self.grade = "B"
		elif self.average >= 70:
			self.grade = "C"
		elif self.average >= 60:
			self.grade = "D"
		else:
			self.grade = "F"

	def to_file_format(self):
		return (
			f"{self.name}|{self.student_id}|{self.test1}|{self.test2}|"
			f"{self.test3}|{self.average}|{self.grade}"
		)


def load_students():
	"""Load student records, skipping malformed records with a message."""
	students = []
	if not FILE_NAME.exists():
		return students

	try:
		with FILE_NAME.open("r", encoding="utf-8") as file:
			for line_number, line in enumerate(file, start=1):
				parts = line.rstrip("\n").split("|")
				if len(parts) != 7:
					print(f"Warning: skipped invalid record on line {line_number}.")
					continue
				try:
					students.append(
						Student(
							parts[0],
							parts[1],
							float(parts[2]),
							float(parts[3]),
							float(parts[4]),
						)
					)
				except ValueError:
					print(f"Warning: skipped invalid scores on line {line_number}.")
	except OSError as error:
		print(f"Could not load student records: {error}")
	return students


def save_students(students):
	"""Save all records in the required pipe-delimited format."""
	print("Saving records...")
	try:
		with FILE_NAME.open("w", encoding="utf-8") as file:
			for student in students:
				file.write(student.to_file_format() + "\n")
		print(f"✓ Saved {len(students)} student record(s) to file.")
		print("Thank you for using Student Grade Calculator!")
	except OSError as error:
		print(f"Could not save student records: {error}")


def get_score(test_number):
	while True:
		try:
			score = float(input(f"Enter Test {test_number} score: "))
			if 0 <= score <= 100:
				return score
			print("Please enter a score from 0 to 100.")
		except ValueError:
			print("Please enter a valid number.")


def add_student(students):
	print("\n" + "=" * 60)
	print("ADD NEW STUDENT")
	print("=" * 60)
	name = input("Enter student name: ").strip()
	student_id = input("Enter student ID: ").strip()
	if not name or not student_id:
		print("Name and student ID are required.")
		return

	student = Student(
		name,
		student_id,
		get_score(1),
		get_score(2),
		get_score(3),
	)
	students.append(student)
	print(f"\n✓ Added student: {student.name} (ID: {student.student_id})")
	print(f"    Average: {student.average:.2f} | Grade: {student.grade}")


def display_students(students):
	if not students:
		print("No student records found.")
		return

	print("\n" + "=" * 60)
	print("ALL STUDENT RECORDS")
	print("=" * 60)
	print(
		f"{'Name':<20}{'ID':<10}{'Test 1':>9}{'Test 2':>9}"
		f"{'Test 3':>9}{'Average':>9}{'Grade':>7}"
	)
	print("-" * 73)
	for student in students:
		print(
			f"{student.name:<20.20}{student.student_id:<10.10}"
			f"{student.test1:>9.2f}{student.test2:>9.2f}"
			f"{student.test3:>9.2f}{student.average:>9.2f}"
			f"{student.grade:>7}"
		)
	print("=" * 73)
	print(f"Total students: {len(students)}")


def display_statistics(students):
	if not students:
		print("No student records available for statistics.")
		return

	highest = max(students, key=lambda student: student.average)
	lowest = min(students, key=lambda student: student.average)
	class_average = sum(student.average for student in students) / len(students)
	grade_counts = {}
	for student in students:
		grade_counts[student.grade] = grade_counts.get(student.grade, 0) + 1

	print("\n" + "=" * 60)
	print("CLASS STATISTICS")
	print("=" * 60)
	print(f"\nClass Average: {class_average:.2f}")
	print(f"Highest Average: {highest.average:.2f} ({highest.name})")
	print(f"Lowest Average: {lowest.average:.2f} ({lowest.name})")
	print("\nGrade Distribution:")
	for grade, count in sorted(grade_counts.items(), key=lambda item: item[1], reverse=True):
		print(f"    {grade}: {count} student(s)")


def search_students(students):
	print("\n" + "=" * 60)
	print("SEARCH STUDENT")
	print("=" * 60)
	search_name = input("Enter student name to search: ").strip()
	matches = [
		student for student in students if search_name.lower() in student.name.lower()
	]
	if not matches:
		print(f"No student found with name: {search_name.lower()}")
		return

	for student in matches:
		print("\nFound student:")
		print(f"    Name: {student.name}")
		print(f"    ID: {student.student_id}")
		print(f"    Test 1: {student.test1:.2f}")
		print(f"    Test 2: {student.test2:.2f}")
		print(f"    Test 3: {student.test3:.2f}")
		print(f"    Average: {student.average:.2f}")
		print(f"    Grade: {student.grade}")


def display_menu():
	print("\n" + "=" * 60)
	print("STUDENT GRADE CALCULATOR")
	print("=" * 60)
	print("1. Add New Student")
	print("2. Display All Students")
	print("3. Search Student by Name")
	print("4. View Class Statistics")
	print("5. Save and Exit (or press ESC)")
	print("=" * 60)


def main():
	Intro()
	students = load_students()

	while True:
		display_menu()
		choice = input("Select an option (1-5) or press ESC to exit: ").strip()
		if choice.lower() in {"esc", "\x1b"}:
			save_students(students)
			break
		if choice == "1":
			add_student(students)
		elif choice == "2":
			display_students(students)
		elif choice == "3":
			search_students(students)
		elif choice == "4":
			display_statistics(students)
		elif choice == "5":
			save_students(students)
			break
		else:
			print("Invalid choice. Select 1-5 or ESC to exit.")


if __name__ == "__main__":
	main()
