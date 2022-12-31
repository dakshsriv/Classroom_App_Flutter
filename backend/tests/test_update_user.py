import sqlite3, requests, uuid, json

def test_update_student():
    conn = sqlite3.connect("../classroom.db")
    cursor = conn.cursor()
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())
    _ = requests.post("https://dev.dakshsrivastava.com/register", json = {"name": username, "password": password, "account_type": "Student"}, verify=False)
    x = requests.post("https://dev.dakshsrivastava.com/login", json = {"name": username, "password": password}, verify=False)
    ret = json.loads(x.text)
    if ret["id"] == "NULL":
        assert False, "Login unsuccessful"
    _ = requests.put(f"https://dev.dakshsrivastava.com/register/{ret['id']}", json = {"name": username, "password": "password"}, verify=False)
    cursor.execute("SELECT * FROM Students WHERE NAME=? AND PASSWORD=?", (username, "password"))
    res = cursor.fetchall()
    assert (not not res), f"res was {res, ret['id']}"
    cursor.execute("DELETE FROM Students WHERE NAME=? AND PASSWORD=?", (username, "password"))
    conn.commit()
    conn.close()

def test_update_teacher():
    conn = sqlite3.connect("../classroom.db")
    cursor = conn.cursor()
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())
    _ = requests.post("https://dev.dakshsrivastava.com/register", json = {"name": username, "password": password, "account_type": "Teacher"}, verify=False)
    x = requests.post("https://dev.dakshsrivastava.com/login", json = {"name": username, "password": password}, verify=False)
    ret = json.loads(x.text)
    if ret["id"] == "NULL":
        assert False, "Login unsuccessful"
    ret = json.loads(x.text)
    _ = requests.put(f"https://dev.dakshsrivastava.com/register/{ret['id']}", json = {"name": username, "password": "password"}, verify=False)
    cursor.execute("SELECT * FROM Teachers WHERE NAME=? AND PASSWORD=?", (username, "password"))
    res = cursor.fetchall()
    assert (not not res), f"res was {res}"
    cursor.execute("DELETE FROM Teachers WHERE NAME=? AND PASSWORD=?", (username, "password"))
    conn.commit()
    conn.close()
