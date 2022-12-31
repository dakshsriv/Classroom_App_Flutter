import sqlite3, requests, json

def test_submit_assignment():
    conn = sqlite3.connect("../classroom.db")
    cursor = conn.cursor()
    x0 = requests.post("https://dev.dakshsrivastava.com/register", json = {"name": "test_get_students_in_clas", "password": "test_get_students_in_clas", "account_type": "Teacher"}, verify=False)
    teacher_id = json.loads(x0.text)["id"]
    x1 = requests.post("https://dev.dakshsrivastava.com/register", json = {"name": "username", "password": "password", "account_type": "Student"}, verify=False)
    student_id = json.loads(x1.text)["id"]
    x2 = requests.post("https://dev.dakshsrivastava.com/classrooms/", json={"title": "test_get_teacher_classrooms", "description": "test_get_teacher_classrooms", "teacher_id":teacher_id}, verify=False)
    class_id = json.loads(x2.text)["id"]
    _ = requests.post("https://dev.dakshsrivastava.com/classes/", json={"student_id": student_id, "class_id": class_id}, verify=False)
    x3 = requests.post(f"https://dev.dakshsrivastava.com/assignments/{class_id}", json={"name": "Test Assignment", "description": "Sample Description", "teacher_id":teacher_id, "class_id": class_id}, verify=False)
    assignment_id = json.loads(x3.text)["id"]
    cursor.execute("INSERT INTO StudentsToClassrooms (STUDENT_ID, CLASSROOM_ID) VALUES (?, ?)", (student_id, class_id))
    conn.commit()
    cursor.execute("UPDATE SubmitAssignments SET STATUS=0 WHERE STUDENT_ID=? AND ASSIGNMENT_ID=?", (student_id, assignment_id))
    conn.commit()
    _ = requests.post(f"https://dev.dakshsrivastava.com/submit/", json={"student_id":student_id, "assignment_id":assignment_id}, verify=False)
    cursor.execute("SELECT STATUS FROM SubmitAssignments WHERE STUDENT_ID=? AND ASSIGNMENT_ID=?", (student_id, assignment_id))
    res = cursor.fetchall()


    cursor.execute("DELETE FROM Classrooms WHERE ID=?", (class_id,))
    cursor.execute("DELETE FROM Teachers WHERE ID=?", (teacher_id,))
    cursor.execute("DELETE FROM Students WHERE ID=?", (student_id,))
    cursor.execute("DELETE FROM StudentsToClassrooms WHERE STUDENT_ID=? AND CLASSROOM_ID=?", (student_id, class_id))

    cursor.execute("DELETE FROM Assignments WHERE ID=?", (assignment_id,))
    conn.commit()
    conn.close()
    assert (res[0][0] == 1), res