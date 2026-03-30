import csv
import os
import numpy as np
import matplotlib.pyplot as plt


class Student:
    def __init__(self, roll, name, father, marks):
        self.roll = roll
        self.name = name
        self.father = father
        self.subjects = ['Python', 'DWD', 'COA', 'PMOB', 'Math']
        self.marks = np.array(marks, dtype=float)

    def total(self):
        return np.sum(self.marks)

    def percentage(self):
        return (self.total() / (len(self.marks) * 100)) * 100

    def cgpa(self):
        return min(round(self.percentage() / 9.5, 2), 10)

    def result(self):
        return "Pass" if np.all(self.marks >= 40) else "Fail"

    def grade(self):
        p = self.percentage()

        if p >= 90:
            return "A+"
        elif p >= 80:
            return "A"
        elif p >= 70:
            return "B"
        elif p >= 60:
            return "C"
        elif p >= 50:
            return "D"
        else:
            return "F"


class StudentManager:
    def __init__(self, filename="student_records.csv"):
        self.filename = filename
        self.students = []
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if row and len(row) >= 8:
                        roll = row[0]
                        name = row[1]
                        father = row[2]
                        marks = list(map(float, row[3:8]))
                        self.students.append(Student(roll, name, father, marks))

    def save_data(self):
        if not self.students:
            print("No student records to save!")
            return

        sorted_students = sorted(self.students, key=lambda x: x.total(), reverse=True)

        with open(self.filename, 'w', newline="") as f:
            writer = csv.writer(f)

            writer.writerow([
                "Roll No", "Name", "Father Name",
                "Python", "DWD", "COA", "PMOB", "Math",
                "Total", "Percentage", "CGPA", "Grade", "Result"
            ])

            for s in sorted_students:
                writer.writerow([
                    s.roll, s.name, s.father, *s.marks,
                    s.total(),
                    round(s.percentage(), 2),
                    s.cgpa(),
                    s.grade(),
                    s.result()
                ])

        print("Data saved successfully!")

    def add_students(self):
        n = int(input("Enter number of students: "))

        for _ in range(n):
            roll = input("Enter Roll No: ")
            name = input("Enter Name: ")
            father = input("Enter Father's Name: ")

            marks = []
            for sub in ['Python', 'DWD', 'COA', 'PMOB', 'Math']:
                while True:
                    try:
                        mark = float(input(f"Enter marks for {sub}: "))
                        if 0 <= mark <= 100:
                            marks.append(mark)
                            break
                        else:
                            print("Enter marks between 0 and 100.")
                    except ValueError:
                        print("Invalid input!")

            self.students.append(Student(roll, name, father, marks))
            print(f"{name} added successfully!\n")

        self.save_data()

    def view_students(self):
        if not self.students:
            print("No records found!")
            return

        sorted_students = sorted(self.students, key=lambda x: x.total(), reverse=True)

        print("\nStudent Record Table")
        print("-" * 120)

        for s in sorted_students:
            print(f"{s.roll} | {s.name} | {s.total()} | {s.percentage():.2f}% | {s.grade()} | {s.result()}")

        print("-" * 120)

    def analyze_class(self):
        if not self.students:
            print("No records available!")
            return

        percentages = np.array([s.percentage() for s in self.students])
        names = [s.name for s in self.students]

        print("\n--- Class Performance ---")
        print(f"Highest: {np.max(percentages):.2f}%")
        print(f"Lowest: {np.min(percentages):.2f}%")
        print(f"Average: {np.mean(percentages):.2f}%")

        # Bar chart
        plt.figure(figsize=(8, 4))
        plt.bar(names, percentages)
        plt.xticks(rotation=45)
        plt.title("Student Performance")
        plt.show()


def main():
    manager = StudentManager()

    while True:
        print("\nStudent Record System")
        print("1. Add Students")
        print("2. View Students")
        print("3. Analyze Class")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            manager.add_students()
        elif choice == "2":
            manager.view_students()
        elif choice == "3":
            manager.analyze_class()
        elif choice == "4":
            manager.save_data()
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
