import sqlite3, requests, uuid, json


def test_create_classroom_pass():
    conn = sqlite3.connect("../classroom.db")
    cursor = conn.cursor()
    title = str(uuid.uuid4())
    description = str(uuid.uuid4())
    x0 = requests.post("https://dev.dakshsrivastava.com/register", json = {"name": "username1", "password": "password1", "account_type": "Teacher"}, verify=False)
    teacher_id = json.loads(x0.text)["id"]
    _ = requests.post("https://dev.dakshsrivastava.com/classrooms", json={"title": title, "description": description, "teacher_id":teacher_id}, verify=False)
    #cursor.execute("SELECT * FROM Classrooms WHERE TITLE=? AND DESCRIPTION=? AND TEACHER_ID=?", (title, description, teacher_id))
    cursor.execute("SELECT TITLE, DESCRIPTION, TEACHER_ID FROM Classrooms WHERE TEACHER_ID=?", (teacher_id,))
    res = cursor.fetchall()
    cursor.execute("DELETE FROM Classrooms WHERE TITLE=? AND DESCRIPTION=? AND TEACHER_ID=?", (title, description, teacher_id))
    cursor.execute("DELETE FROM Teachers WHERE ID=?", (teacher_id,))
    conn.commit()
    conn.close()
    assert (res[0][0] == title and res[0][1] == description and res[0][2] == teacher_id), f"Res: {res}, title: {title}, description: {description}, teacherID: {teacher_id}"


def test_create_classroom_not_teacher():
    conn = sqlite3.connect("../classroom.db")
    cursor = conn.cursor()
    title = str(uuid.uuid4())
    description = str(uuid.uuid4())
    x0 = requests.post("https://dev.dakshsrivastava.com/register", json = {"name": "username", "password": "password", "account_type": "Student"}, verify=False)
    student_id = json.loads(x0.text)["id"]
    x = requests.post("https://dev.dakshsrivastava.com/classrooms", json={"title": title, "description": description, "teacher_id":student_id}, verify=False)
    cursor.execute("DELETE FROM Classrooms WHERE TITLE=? AND DESCRIPTION=? AND TEACHER_ID=?", (title, description, student_id))
    cursor.execute("DELETE FROM Students WHERE ID=?", (student_id,))
    conn.commit()
    conn.close()
    assert (x.status_code == 400)


def test_create_classroom_exists():
    conn = sqlite3.connect("../classroom.db")
    cursor = conn.cursor()
    title = str(uuid.uuid4())
    description = str(uuid.uuid4())
    x0 = requests.post("https://dev.dakshsrivastava.com/register", json = {"name": "username", "password": "password", "account_type": "Teacher"}, verify=False)
    teacher_id = json.loads(x0.text)["id"]
    _ = requests.post("https://dev.dakshsrivastava.com/classrooms", json={"title": title, "description": description, "teacher_id":teacher_id}, verify=False)
    ###
    x = requests.post("https://dev.dakshsrivastava.com/classrooms", json={"title": title, "description": description, "teacher_id":teacher_id}, verify=False)
    ###
    cursor.execute("DELETE FROM Classrooms WHERE TITLE=? AND DESCRIPTION=? AND TEACHER_ID=?", (title, description, teacher_id))
    cursor.execute("DELETE FROM Teachers WHERE ID=?", (teacher_id,))
    conn.commit()
    conn.close()
    assert (x.status_code == 400) 