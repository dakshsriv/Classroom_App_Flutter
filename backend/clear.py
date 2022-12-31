import sqlite3

conn = sqlite3.connect("../backend/classroom.db")
cursor = conn.cursor()

cursor.execute('DELETE FROM Teachers;')
cursor.execute('DELETE FROM Assignments;')
cursor.execute('DELETE FROM Students;')
cursor.execute('DELETE FROM Classrooms;')
cursor.execute('DELETE FROM StudentsToClassrooms;')
cursor.execute('DELETE FROM SubmitAssignments;')

conn.commit()