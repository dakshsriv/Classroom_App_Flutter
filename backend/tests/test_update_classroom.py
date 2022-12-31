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
    _ = requests.put(f"https://dev.dakshsrivastava.com/classrooms/{class_id}", json={"title": title, "description": "This is what should be seen", "teacher_id":teacher_id}, verify=False)
    cursor.execute("SELECT DESCRIPTION FROM Classrooms")
    res = cursor.fetchall()
    cursor.execute("DELETE FROM Classrooms WHERE TITLE=? AND DESCRIPTION=? AND TEACHER_ID=?", (title, "This is what should be seen", teacher_id))
    cursor.execute("DELETE FROM Teachers WHERE ID=?", (teacher_id,))
    conn.commit()
    conn.close()
    assert (res[0][0] == "This is what should be seen"), f"res is {res}"


def test_update_classroom_unauthorized():
    conn = sqlite3.connect("../classroom.db")
    cursor = conn.cursor()
    title = "Sample"
    description = "Ample"
    x0 = requests.post("https://dev.dakshsrivastava.com/register", json = {"name": "username", "password": "password", "account_type": "Teacher"}, verify=False)
    teacher_id = json.loads(x0.text)["id"]
    x1 = requests.post("https://dev.dakshsrivastava.com/classrooms", json={"title": title, "description": description, "teacher_id":teacher_id}, verify=False)
    class_id = json.loads(x1.text)["id"]
    x = requests.put(f"https://dev.dakshsrivastava.com/classrooms/{class_id}", json={"title": title, "description": "This is what should be seen", "teacher_id":"invalid"}, verify=False)
    cursor.execute("DELETE FROM Classrooms WHERE TITLE=? AND DESCRIPTION=? AND TEACHER_ID=?", (title, description, teacher_id))
    cursor.execute("DELETE FROM Teachers WHERE ID=?", (teacher_id,))
    conn.commit()
    conn.close()
    assert (x.status_code == 400)


def test_update_classroom_not_exists():
    title = str(uuid.uuid4())
    description = str(uuid.uuid4())
    teacher_id = "Won't work"
    class_id = "Fake"
    _ = requests.post("https://dev.dakshsrivastava.com/classrooms", json={"title": title, "description": description, "teacher_id":teacher_id}, verify=False)
    x = requests.put(f"https://dev.dakshsrivastava.com/classrooms/{class_id}", json={"title": title, "description": "This is what should be seen", "teacher_id":"invalid"}, verify=False)
    assert (x.status_code == 400)
