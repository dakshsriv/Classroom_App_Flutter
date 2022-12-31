import sqlite3, requests, json

def test_get_classes():
    conn = sqlite3.connect("../classroom.db")
    cursor = conn.cursor()
    x0 = requests.post("https://dev.dakshsrivastava.com/register", json = {"name": "test_get_students_in_clas", "password": "test_get_students_in_clas", "account_type": "Teacher"}, verify=False)
    teacher_id = json.loads(x0.text)["id"]
    x1 = requests.post("https://dev.dakshsrivastava.com/register", json = {"name": "username", "password": "password", "account_type": "Student"}, verify=False)
    student_id = json.loads(x1.text)["id"]
    x2 = requests.post("https://dev.dakshsrivastava.com/classrooms/", json={"title": "test_get_teacher_classrooms", "description": "test_get_teacher_classrooms", "teacher_id":teacher_id}, verify=False)
    class_id = json.loads(x2.text)["id"]
    cursor.execute("INSERT INTO StudentsToClassrooms (STUDENT_ID, CLASSROOM_ID) VALUES (?, ?)", (student_id, class_id))
    conn.commit()
    x = requests.get(f"https://dev.dakshsrivastava.com/classes/{student_id}", verify=False)
    info = json.loads(x.text)
    #cursor.execute("SELECT NAME FROM StudentsToClassrooms WHERE CLASSROOM_ID=? ", (class_id,))
    ###
    cursor.execute(
        "SELECT CLASSROOM_ID FROM StudentsToClassrooms WHERE STUDENT_ID=?;",
        (student_id,)
    )
    rows = cursor.fetchall()
    rowstosend = list()
    for fid in rows:
        id = fid[0]
        cursor.execute("SELECT * FROM Classrooms WHERE ID=?;", (id,))
        rows2 = cursor.fetchall()
        print("Testing")
        rowstosend.append(rows2[0])
    ###
    cursor.execute("DELETE FROM Classrooms WHERE ID=?", (class_id,))
    cursor.execute("DELETE FROM Teachers WHERE ID=?", (teacher_id,))
    cursor.execute("DELETE FROM Students WHERE ID=?", (student_id,))
    cursor.execute("DELETE FROM StudentsToClassrooms WHERE STUDENT_ID=? AND CLASSROOM_ID=?", (student_id, class_id))
    conn.commit()
    conn.close()
    assert (info[0][0] == rowstosend[0][0])