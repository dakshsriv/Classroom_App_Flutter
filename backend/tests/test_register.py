import sqlite3, requests, uuid


def test_register_student():
    conn = sqlite3.connect("../classroom.db")
    cursor = conn.cursor()
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())
    _ = requests.post("https://dev.dakshsrivastava.com/register", json = {"name": username, "password": password, "account_type": "Student"}, verify=False)
    cursor.execute("SELECT * FROM Students WHERE NAME=? AND PASSWORD=?", (username, password))
    res = cursor.fetchall()
    print(res)
    assert (not not res), f"res was {res}"
    x = requests.post("https://dev.dakshsrivastava.com/register", json = {"name": username, "password": password, "account_type": "Student"}, verify=False)
    assert (x.status_code==400)
    cursor.execute("DELETE FROM Students WHERE NAME=? AND PASSWORD=?", (username, password))
    conn.commit()
    conn.close()

def test_register_teacher():
    conn = sqlite3.connect("../classroom.db")
    cursor = conn.cursor()
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())
    _ = requests.post("https://dev.dakshsrivastava.com/register", json = {"name": username, "password": password, "account_type": "Teacher"}, verify=False)
    cursor.execute("SELECT * FROM Teachers WHERE NAME=? AND PASSWORD=?", (username, password))
    res = cursor.fetchall()
    print(res)
    assert (not not res), f"res was {res}"
    x = requests.post("https://dev.dakshsrivastava.com/register", json = {"name": username, "password": password, "account_type": "Teacher"}, verify=False)
    assert (x.status_code==400)
    cursor.execute("DELETE FROM Teachers WHERE NAME=? AND PASSWORD=?", (username, password))
    conn.commit()
    conn.close()

