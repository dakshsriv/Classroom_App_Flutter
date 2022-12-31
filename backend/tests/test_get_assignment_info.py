import sqlite3, requests, json


def test_get_assignment_info_pass():
    conn = sqlite3.connect("../classroom.db")
    cursor = conn.cursor()
    title = "The title stays the same"
    description = "I shouldn't be seeing this."
    x0 = requests.post("https://dev.dakshsrivastava.com/register", json = {"name": "username", "password": "password", "account_type": "Teacher"}, verify=False)
    teacher_id = json.loads(x0.text)["id"]
    x1 = requests.post("https://dev.dakshsrivastava.com/classrooms", json={"title": title, "description": description, "teacher_id":teacher_id}, verify=False)
    class_id = json.loads(x1.text)["id"]
    x2 = requests.post(f"https://dev.dakshsrivastava.com/assignments/{class_id}", json={"name": "Test Assignment", "description": "Sample Description", "teacher_id":teacher_id, "class_id": class_id}, verify=False)
    assignment_id = json.loads(x2.text)["id"]
    x = requests.get(f"https://dev.dakshsrivastava.com/assignments/{assignment_id}", verify=False)
    res = json.loads(x.text)
    cursor.execute("DELETE FROM Classrooms WHERE ID=?", (class_id,))
    cursor.execute("DELETE FROM Teachers WHERE ID=?", (teacher_id,))
    cursor.execute("DELETE FROM Assignments WHERE NAME=? AND DESCRIPTION=? AND CLASS_ID=?", ("Test Assignment", "Sample Description", class_id))
    conn.commit()
    conn.close()
    assert (res[0][0] == assignment_id and res[0][1] == "Test Assignment" and res[0][2] == "Sample Description"), f"Res is {res}"
