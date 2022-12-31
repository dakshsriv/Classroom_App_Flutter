import sqlite3, requests, json

def test_join_class_pass():
    conn = sqlite3.connect("../classroom.db")
    cursor = conn.cursor()
    x0 = requests.post("https://dev.dakshsrivastava.com/register", json = {"name": "test_get_students_in_clas", "password": "test_get_students_in_clas", "account_type": "Teacher"}, verify=False)
    teacher_id = json.loads(x0.text)["id"]
    x1 = requests.post("https://dev.dakshsrivastava.com/register", json = {"name": "username", "password": "password", "account_type": "Student"}, verify=False)
    student_id = json.loads(x1.text)["id"]
    x2 = requests.post("https://dev.dakshsrivastava.com/classrooms/", json={"title": "test_get_teacher_classrooms", "description": "test_get_teacher_classrooms", "teacher_id":teacher_id}, verify=False)
    class_id = json.loads(x2.text)["id"]
    _ = requests.post("https://dev.dakshsrivastava.com/classes/", json={"student_id": student_id, "class_id": class_id}, verify=False)
    cursor.execute("SELECT * FROM StudentsToClassrooms WHERE STUDENT_ID=? AND CLASSROOM_ID=?", (student_id, class_id))
    res = cursor.fetchall()
    #cursor.execute("SELECT NAME FROM StudentsToClassrooms WHERE CLASSROOM_ID=? ", (class_id,))
    ###
    ###
    cursor.execute("DELETE FROM Classrooms WHERE ID=?", (class_id,))
    cursor.execute("DELETE FROM Teachers WHERE ID=?", (teacher_id,))
    cursor.execute("DELETE FROM Students WHERE ID=?", (student_id,))
    cursor.execute("DELETE FROM StudentsToClassrooms WHERE STUDENT_ID=? AND CLASSROOM_ID=?", (student_id, class_id))
    conn.commit()
    conn.close()
    assert (res == [(student_id, class_id)])

def test_join_class_fail():
    conn = sqlite3.connect("../classroom.db")
    cursor = conn.cursor()
    x0 = requests.post("https://dev.dakshsrivastava.com/register", json = {"name": "test_get_students_in_clas", "password": "test_get_students_in_clas", "account_type": "Teacher"}, verify=False)
    teacher_id = json.loads(x0.text)["id"]
    x1 = requests.post("https://dev.dakshsrivastava.com/register", json = {"name": "username", "password": "password", "account_type": "Student"}, verify=False)
    student_id = json.loads(x1.text)["id"]
    x2 = requests.post("https://dev.dakshsrivastava.com/classrooms/", json={"title": "test_get_teacher_classrooms", "description": "test_get_teacher_classrooms", "teacher_id":teacher_id}, verify=False)
    class_id = json.loads(x2.text)["id"]
    x = requests.post("https://dev.dakshsrivastava.com/classes/", json={"student_id": student_id, "class_id": "Must fail"}, verify=False)
    #cursor.execute("SELECT NAME FROM StudentsToClassrooms WHERE CLASSROOM_ID=? ", (class_id,))
    ###
    ###
    cursor.execute("DELETE FROM Classrooms WHERE ID=?", (class_id,))
    cursor.execute("DELETE FROM Teachers WHERE ID=?", (teacher_id,))
    cursor.execute("DELETE FROM Students WHERE ID=?", (student_id,))
    cursor.execute("DELETE FROM StudentsToClassrooms WHERE STUDENT_ID=? AND CLASSROOM_ID=?", (student_id, class_id))
    conn.commit()
    conn.close()
    assert (x.status_code == 400)