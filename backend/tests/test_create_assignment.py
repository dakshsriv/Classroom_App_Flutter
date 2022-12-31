import sqlite3, requests, uuid, json

def test_create_assignment_pass():
    conn = sqlite3.connect("../classroom.db")
    cursor = conn.cursor()
    title = str(uuid.uuid4())
    description = str(uuid.uuid4())
    x0 = requests.post("https://dev.dakshsrivastava.com/register", json = {"name": "username1", "password": "password1", "account_type": "Teacher"}, verify=False)
    teacher_id = json.loads(x0.text)["id"]
    x1 = requests.post("https://dev.dakshsrivastava.com/classrooms", json={"title": title, "description": description, "teacher_id":teacher_id}, verify=False)
    class_id = json.loads(x1.text)["id"]
    _ = requests.post(f"https://dev.dakshsrivastava.com/assignments/{class_id}", json={"name": "Test Assignment", "description": "Sample Description", "teacher_id":teacher_id, "class_id": class_id}, verify=False)
    cursor.execute("SELECT NAME, DESCRIPTION, CLASS_ID FROM Assignments WHERE NAME=? AND DESCRIPTION=? AND CLASS_ID=?", ("Test Assignment", "Sample Description", class_id))
    res = cursor.fetchall()
    cursor.execute("DELETE FROM Classrooms WHERE ID=?", (class_id,))
    cursor.execute("DELETE FROM Teachers WHERE ID=?", (teacher_id,))
    cursor.execute("DELETE FROM Assignments WHERE NAME=? AND DESCRIPTION=? AND CLASS_ID=?", ("Test Assignment", "Sample Description", class_id))
    conn.commit()
    conn.close()
    assert (res[0] == ("Test Assignment", "Sample Description", class_id)), f"Res: {res}"


def test_create_assignment_unauthorized():
    conn = sqlite3.connect("../classroom.db")
    cursor = conn.cursor()
    title = str(uuid.uuid4())
    description = str(uuid.uuid4())
    x0 = requests.post("https://dev.dakshsrivastava.com/register", json = {"name": "username1", "password": "password1", "account_type": "Teacher"}, verify=False)
    teacher_id = json.loads(x0.text)["id"]
    x1 = requests.post("https://dev.dakshsrivastava.com/classrooms", json={"title": title, "description": description, "teacher_id":teacher_id}, verify=False)
    class_id = json.loads(x1.text)["id"]
    x = requests.post(f"https://dev.dakshsrivastava.com/assignments/{class_id}", json={"name": "Test Assignment1", "description": "Sample Description1", "teacher_id":"Shouldn't work", "class_id": class_id}, verify=False)

    cursor.execute("SELECT NAME, DESCRIPTION, CLASS_ID FROM Assignments WHERE NAME=? AND DESCRIPTION=? AND CLASS_ID=?", ("Test Assignment", "Sample Description", class_id))
    res = cursor.fetchall()
    cursor.execute("DELETE FROM Classrooms WHERE ID=?", (class_id,))
    cursor.execute("DELETE FROM Teachers WHERE ID=?", (teacher_id,))
    conn.commit()
    conn.close()
    assert (x.status_code == 400)


def test_create_assignment_exists():
    conn = sqlite3.connect("../classroom.db")
    cursor = conn.cursor()
    title = str(uuid.uuid4())
    description = str(uuid.uuid4())
    id = str(uuid.uuid4())
    x0 = requests.post("https://dev.dakshsrivastava.com/register", json = {"name": "username1", "password": "password1", "account_type": "Teacher"}, verify=False)
    teacher_id = json.loads(x0.text)["id"]
    x1 = requests.post("https://dev.dakshsrivastava.com/classrooms", json={"title": title, "description": description, "teacher_id":teacher_id}, verify=False)
    class_id = json.loads(x1.text)["id"]
    cursor.execute("INSERT INTO Assignments (ID, NAME, DESCRIPTION, CLASS_ID) VALUES (?,?,?,?)", (id, "Test Assignment2", "Sample Description2", class_id))
    conn.commit()
    x = requests.post(f"https://dev.dakshsrivastava.com/assignments/{class_id}", json={"name": "Test Assignment2", "description": "Sample Description2", "teacher_id":teacher_id, "class_id": class_id}, verify=False)
    cursor.execute("DELETE FROM Classrooms WHERE ID=?", (class_id,))
    cursor.execute("DELETE FROM Teachers WHERE ID=?", (teacher_id,))
    cursor.execute("DELETE FROM Assignments WHERE ID=?", (id,))
    conn.commit()
    conn.close()
    assert (x.status_code == 400) 