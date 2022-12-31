import sqlite3, requests, uuid, json

def test_delete_assignment_pass():
    conn = sqlite3.connect("../classroom.db")
    cursor = conn.cursor()
    title = str(uuid.uuid4())
    description = str(uuid.uuid4())
    x0 = requests.post("https://dev.dakshsrivastava.com/register", json = {"name": "username1", "password": "password1", "account_type": "Teacher"}, verify=False)
    teacher_id = json.loads(x0.text)["id"]
    x1 = requests.post("https://dev.dakshsrivastava.com/classrooms", json={"title": title, "description": description, "teacher_id":teacher_id}, verify=False)
    class_id = json.loads(x1.text)["id"]
    x = requests.post(f"https://dev.dakshsrivastava.com/assignments/{class_id}", json={"name": "Test Assignment", "description": "Sample Description", "teacher_id":teacher_id, "class_id": class_id}, verify=False)
    assignment_id = json.loads(x.text)["id"]
    y = requests.delete(f"https://dev.dakshsrivastava.com/assignments/{assignment_id}/", verify=False)
    cursor.execute("SELECT DESCRIPTION FROM Assignments WHERE NAME=? AND DESCRIPTION=? AND CLASS_ID=?", ("Test Assignment", "New Description", class_id))
    res = cursor.fetchall()
    cursor.execute("DELETE FROM Classrooms WHERE ID=?", (class_id,))
    cursor.execute("DELETE FROM Teachers WHERE ID=?", (teacher_id,))
    cursor.execute("DELETE FROM Assignments WHERE NAME=? AND CLASS_ID=?", ("Test Assignment", class_id))
    conn.commit()
    conn.close()
    assert (not res and y.status_code == 204), f"Res: {res}, stats-code {y.status_code}"


def test_delete_assignment_unauthorized():
    conn = sqlite3.connect("../classroom.db")
    cursor = conn.cursor()
    title = str(uuid.uuid4())
    description = str(uuid.uuid4())
    x0 = requests.post("https://dev.dakshsrivastava.com/register", json = {"name": "username1", "password": "password1", "account_type": "Teacher"}, verify=False)
    teacher_id = json.loads(x0.text)["id"]
    x1 = requests.post("https://dev.dakshsrivastava.com/classrooms", json={"title": title, "description": description, "teacher_id":teacher_id}, verify=False)
    class_id = json.loads(x1.text)["id"]
    x = requests.post(f"https://dev.dakshsrivastava.com/assignments/{class_id}", json={"name": "Test Assignment", "description": "Sample Description", "teacher_id":teacher_id, "class_id": class_id}, verify=False)
    assignment_id = json.loads(x.text)["id"]
    y = requests.delete(f"https://dev.dakshsrivastava.com/assignments/{class_id}/", verify=False)
    cursor.execute("SELECT DESCRIPTION FROM Assignments WHERE NAME=? AND DESCRIPTION=? AND CLASS_ID=?", ("Test Assignment", "New Description", class_id))
    res = cursor.fetchall()
    cursor.execute("DELETE FROM Classrooms WHERE ID=?", (class_id,))
    cursor.execute("DELETE FROM Teachers WHERE ID=?", (teacher_id,))
    cursor.execute("DELETE FROM Assignments WHERE NAME=? AND CLASS_ID=?", ("Test Assignment", class_id))
    conn.commit()
    conn.close()
    assert (y.status_code == 400), f"Res: {res}"
