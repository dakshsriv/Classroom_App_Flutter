import sqlite3, requests, uuid, json


def test_update_classroom_pass():
    conn = sqlite3.connect("../classroom.db")
    cursor = conn.cursor()
    title = "The title stays the same"
    description = "I shouldn't be seeing this."
    x0 = requests.post("https://dev.dakshsrivastava.com/register", json = {"name": "username", "password": "password", "account_type": "Teacher"}, verify=False)
    teacher_id = json.loads(x0.text)["id"]
    x1 = requests.post("https://dev.dakshsrivastava.com/classrooms", json={"title": title, "description": description, "teacher_id":teacher_id}, verify=False)
    class_id = json.loads(x1.text)["id"]
    _ = requests.delete(f"https://dev.dakshsrivastava.com/classrooms/{class_id}", verify=False)
    cursor.execute("SELECT * FROM Classrooms WHERE TITLE=? AND DESCRIPTION=? AND TEACHER_ID=?", (title, "This is what should be seen", teacher_id))
    r = cursor.fetchall()
    cursor.execute("DELETE FROM Teachers WHERE ID=?", (teacher_id,))
    conn.commit()
    conn.close()
    assert (not r), f"R is {r}"


def test_update_classroom_unauthorized():
    conn = sqlite3.connect("../classroom.db")
    cursor = conn.cursor()
    title = "Sample"
    description = "Ample"
    x0 = requests.post("https://dev.dakshsrivastava.com/register", json = {"name": "username", "password": "password", "account_type": "Teacher"}, verify=False)
    teacher_id = json.loads(x0.text)["id"]
    x1 = requests.post("https://dev.dakshsrivastava.com/classrooms", json={"title": title, "description": description, "teacher_id":teacher_id}, verify=False)
    class_id = json.loads(x1.text)["id"]
    x = requests.delete(f"https://dev.dakshsrivastava.com/classrooms/class_id", json={"title": title, "description": "This is what should be seen", "teacher_id":"invalid"}, verify=False)
    cursor.execute("DELETE FROM Classrooms WHERE TITLE=? AND DESCRIPTION=? AND TEACHER_ID=?", (title, description, teacher_id))
    cursor.execute("DELETE FROM Teachers WHERE ID=?", (teacher_id,))
    conn.commit()
    conn.close()
    assert (x.status_code == 400)