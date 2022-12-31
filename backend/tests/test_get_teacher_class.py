import sqlite3, requests, uuid, json

def test_get_teacher_classrooms():
    conn = sqlite3.connect("../classroom.db")
    cursor = conn.cursor()
    x0 = requests.post("https://dev.dakshsrivastava.com/register", json = {"name": "test_get_teacher_classrooms", "password": "test_get_teacher_classrooms", "account_type": "Teacher"}, verify=False)
    teacher_id = json.loads(x0.text)["id"]
    x1 = requests.post("https://dev.dakshsrivastava.com/classrooms", json={"title": "test_get_teacher_classrooms", "description": "test_get_teacher_classrooms", "teacher_id":teacher_id}, verify=False)
    class_id = json.loads(x1.text)["id"]
    x = requests.get(f"https://dev.dakshsrivastava.com/classrooms/teacher/{teacher_id}", verify=False)
    classrooms = [x[0] for x in json.loads(x.text)]
    cursor.execute("SELECT * FROM Classrooms WHERE TEACHER_ID=?;", (teacher_id,))
    target = [x[0] for x in cursor.fetchall()]
    cursor.execute("DELETE FROM Classrooms WHERE ID=?", (class_id,))
    cursor.execute("DELETE FROM Teachers WHERE ID=?", (teacher_id,))
    conn.commit()
    conn.close()
    assert (classrooms == target)

