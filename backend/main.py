from fastapi import FastAPI, APIRouter, Response, status
import uuid
import sqlite3
import models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000/",
    "http://127.0.0.1:3000/",
    "http://192.168.0.28:3000/" "https://localhost:3000/",
    "localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def start_db():
    conn = sqlite3.connect("classroom.db")
    cursor = conn.cursor()
    return conn, cursor


"""
POST: register
"""
########### Working with users


@app.post("/register/", status_code=201)
def register(model: models.Register, response: Response):
    conn, cursor = start_db()
    cursor.execute("SELECT * FROM Students WHERE NAME=?;", (model.name,))
    x = cursor.fetchall()  # Check to see if a student with that name already exists
    cursor.execute("SELECT * FROM Teachers WHERE NAME=?;", (model.name,))
    y = cursor.fetchall()  # Check to see if a student with that name already exists
    if x or y:
        response.status_code = 400
        return
    id = uuid.uuid4()
    if model.account_type == "Student":
        cursor.execute(
            "INSERT INTO Students (ID, NAME, PASSWORD) VALUES (?,?,?);",
            (str(id), model.name, model.password),
        )
        conn.commit()
        conn.close()
        return {"id": id, "name": model.name, "password": model.password}

    elif model.account_type == "Teacher":
        cursor.execute(
            "INSERT INTO Teachers (ID, NAME, PASSWORD) VALUES (?,?,?);",
            (str(id), model.name, model.password),
        )
        conn.commit()
        conn.close()
        return {"id": id, "name": model.name, "password": model.password}
    else:
        response.status_code = 400
        conn.close()
        return


@app.post("/login/", status_code=200)
def login(model: models.Login, response: Response):
    conn, cursor = start_db()
    cursor.execute(
        f"SELECT * FROM Students WHERE NAME=? AND PASSWORD=?;",
        (model.name, model.password),
    )
    rows = cursor.fetchall()
    if not rows:
        cursor.execute(
            f"SELECT * FROM Teachers WHERE NAME=? AND PASSWORD=?;",
            (model.name, model.password),
        )
        rows = cursor.fetchall()
        if not rows:
            conn.close()
            return {"id": "NULL"}
        else:
            conn.close()
            return {"id": rows[0][0], "type": "teacher"}
    else:
        conn.close()
        return {"id": rows[0][0], "type": "student"}


@app.put("/register/{update_id}", status_code=200)
def register(model: models.Login, response: Response, update_id):
    conn, cursor = start_db()
    cursor.execute("SELECT * FROM Students WHERE ID=?;", (update_id,))
    x = cursor.fetchall()  # Check to see if a student with that name already exists
    cursor.execute("SELECT * FROM Teachers WHERE ID=?;", (update_id,))
    y = cursor.fetchall()  # Check to see if a student with that name already exists
    id = uuid.uuid4()
    if x:
        cursor.execute(
            f"UPDATE Students SET NAME=?, PASSWORD=? WHERE ID=?",
            (model.name, model.password, update_id),
        )
        conn.commit()
        conn.close()
        return {"id": update_id, "name": model.name, "password": model.password}
    elif y:
        cursor.execute(
            f"UPDATE Teachers SET NAME=?, PASSWORD=? WHERE ID=?",
            (model.name, model.password, update_id),
        )
        conn.commit()
        conn.close()
        return {"id": update_id, "name": model.name, "password": model.password}
    else:
        response.status_code = 400
        conn.close()
        return


@app.delete("/register/{delete_id}", status_code=204)
def register(response: Response, delete_id):
    conn, cursor = start_db()
    cursor.execute("SELECT * FROM Students WHERE ID=?;", (delete_id,))
    x = cursor.fetchall()  # Check to see if a student with that name already exists
    cursor.execute("SELECT * FROM Teachers WHERE ID=?;", (delete_id,))
    y = cursor.fetchall()  # Check to see if a student with that name already exists
    if x:
        cursor.execute("DELETE FROM Students WHERE ID=?;", (delete_id,))
        conn.commit()
        conn.close()
    elif y:
        cursor.execute("DELETE FROM Teachers WHERE ID=?;", (delete_id,))
        conn.commit()
        conn.close()
    else:
        response.status_code = 400
        conn.close()
        return


########### CRUDding a classroom


@app.get("/classrooms/", status_code=200)
def get_all_classrooms(response: Response):
    conn, cursor = start_db()
    cursor.execute("SELECT ID FROM Classrooms;")
    classrooms = cursor.fetchall()
    conn.close()
    return classrooms


# The above function (deprecated) is just for manual testing purposes


@app.get("/classrooms/teacher/{teacher_id}", status_code=200)
def get_classrooms(response: Response, teacher_id):
    conn, cursor = start_db()
    cursor.execute("SELECT * FROM Classrooms WHERE TEACHER_ID=?;", (teacher_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


@app.get("/classrooms/class/{class_id}", status_code=200)
def get_classrooms(response: Response, class_id):
    conn, cursor = start_db()
    cursor.execute("SELECT * FROM Classrooms WHERE ID=?;", (class_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


@app.get("/classrooms/people/{class_id}", status_code=200)
def get_people(response: Response, class_id):
    conn, cursor = start_db()
    cursor.execute(
        "SELECT NAME, ID FROM StudentsToClassrooms JOIN Students ON Students.ID=StudentsToClassrooms.STUDENT_ID WHERE CLASSROOM_ID=?;",
        (class_id,),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


@app.post("/classrooms/", status_code=201)
def create_classroom(response: Response, model: models.CreateClassroom):
    conn, cursor = start_db()
    cursor.execute(
        "SELECT * FROM Classrooms WHERE TITLE=? AND TEACHER_ID=?;",
        (model.title, model.teacher_id),
    )
    rows = cursor.fetchall()
    cursor.execute("SELECT * FROM Teachers WHERE ID=?", (model.teacher_id,))
    is_teacher = cursor.fetchall()
    if not rows and is_teacher:
        id = uuid.uuid4()
        cursor.execute(
            "INSERT INTO Classrooms (ID, TITLE, DESCRIPTION, TEACHER_ID) VALUES (?,?,?,?)",
            (str(id), model.title, model.description, model.teacher_id),
        )
        conn.commit()
        conn.close()
        return {
            "id": id,
            "title": model.title,
            "description": model.description,
            "teacher_id": model.teacher_id,
        }
    else:
        conn.close()
        response.status_code = 400


@app.put("/classrooms/{update_id}", status_code=200)
def edit_classroom(response: Response, model: models.CreateClassroom, update_id):
    conn, cursor = start_db()
    cursor.execute(
        "SELECT * FROM Classrooms WHERE ID=? AND TEACHER_ID=?;",
        (update_id, model.teacher_id),
    )
    rows = cursor.fetchall()
    if rows:
        cursor.execute(
            "UPDATE Classrooms SET TITLE=?, DESCRIPTION=? WHERE ID=?",
            (
                model.title,
                model.description,
                update_id,
            ),
        )
        conn.commit()
        conn.close()
        return {
            "id": update_id,
            "title": model.title,
            "description": model.description,
            "teacher_id": model.teacher_id,
        }
    else:
        conn.close()
        response.status_code = 400


@app.delete("/classrooms/{delete_id}", status_code=204)
def delete_classroom(response: Response, delete_id):
    conn, cursor = start_db()
    cursor.execute("SELECT * FROM Classrooms WHERE ID=?", (delete_id,))
    x = cursor.fetchall()  # Check to see if a class with that name already exists

    if x:
        cursor.execute("DELETE FROM Classrooms WHERE ID=?;", (delete_id,))
        cursor.execute(
            "DELETE FROM StudentsToClassrooms WHERE CLASSROOM_ID=?;", (delete_id,)
        )
        cursor.execute("DELETE FROM Assignments WHERE CLASS_ID=?;", (delete_id,))
        conn.commit()
        conn.close()
    else:
        response.status_code = 400
        conn.close()
        return


########### Enrollment/Deregistration in a class


@app.get("/classes/{student_id}", status_code=200)
def get_classes(response: Response, student_id):
    conn, cursor = start_db()
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
        rowstosend.append(rows2[0])
    conn.close()
    print(f"Sending: {rowstosend}, fid is {rows}")
    return rowstosend


@app.post("/classes/", status_code=201)
def join_class(response: Response, model: models.AddClass):
    conn, cursor = start_db()
    cursor.execute(
        "SELECT * FROM StudentsToClassrooms WHERE CLASSROOM_ID=? AND STUDENT_ID=?;",
        (model.class_id, model.student_id),
    )
    rows = cursor.fetchall()
    cursor.execute("SELECT * FROM Students WHERE ID=?;", (model.student_id,))
    rows2 = cursor.fetchall()
    cursor.execute("SELECT * FROM Classrooms WHERE ID=?;", (model.class_id,))
    rows3 = cursor.fetchall()
    if not rows and rows2 and rows3:
        cursor.execute(
            "INSERT INTO StudentsToClassrooms (STUDENT_ID, CLASSROOM_ID) VALUES (?,?)",
            (model.student_id, model.class_id),
        )
        cursor.execute("SELECT * FROM Assignments WHERE CLASS_ID=?;", (model.class_id,))
        rows4 = cursor.fetchall()
        assignments = [x[0] for x in rows4]
        for assignment in assignments:
            cursor.execute(
                "INSERT INTO SubmitAssignments (STUDENT_ID, ASSIGNMENT_ID, STATUS) VALUES (?,?,?)",
                (model.student_id, assignment, 0),
            )
        conn.commit()
        conn.close()
        return {"student_id": model.student_id, "class_id": model.class_id}
    else:
        conn.close()
        response.status_code = 400


@app.put("/classes/", status_code=204)
def deregister(response: Response, model: models.AddClass):
    conn, cursor = start_db()
    cursor.execute(
        "SELECT CLASSROOM_ID FROM StudentsToClassrooms WHERE STUDENT_ID=? AND CLASSROOM_ID=?;",
        (model.student_id, model.class_id),
    )
    rows = cursor.fetchall()
    if rows:
        cursor.execute(
            "DELETE FROM StudentsToClassrooms WHERE CLASSROOM_ID=? AND STUDENT_ID=?;",
            (model.class_id, model.student_id),
        )
        cursor.execute("SELECT * FROM Assignments WHERE CLASS_ID=?;", (model.class_id,))
        rows4 = cursor.fetchall()
        assignments = [x[0] for x in rows4]
        for assignment in assignments:
            cursor.execute(
                "DELETE FROM SubmitAssignments WHERE STUDENT_ID=? AND ASSIGNMENT_ID=?",
                (model.student_id, assignment),
            )
        conn.commit()
        conn.close()
    else:
        response.status_code = 400
        conn.close()
        return


########### CRUDding of an Assignment


@app.get("/assignments/class/{class_id}", status_code=200)
def get_classes(response: Response, class_id):
    conn, cursor = start_db()
    cursor.execute(
        "SELECT ID, NAME, DESCRIPTION FROM Assignments WHERE CLASS_ID=?;", (class_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


@app.get("/assignments/{assignment_id}", status_code=200)
def get_classes(response: Response, assignment_id):
    conn, cursor = start_db()
    cursor.execute(
        "SELECT ID, NAME, DESCRIPTION FROM Assignments WHERE ID=?;", (assignment_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


@app.post("/assignments/{class_id}", status_code=201)
def join_class(response: Response, model: models.AddAssignment, class_id):
    conn, cursor = start_db()
    cursor.execute(
        "SELECT * FROM Classrooms WHERE TEACHER_ID=? AND ID=?;",
        (model.teacher_id, model.class_id),
    )
    rows = cursor.fetchall()
    cursor.execute("SELECT * FROM Assignments WHERE DESCRIPTION=? AND CLASS_ID=? AND NAME=?;", (model.description, model.class_id, model.name,))
    rows2 = cursor.fetchall()
    cursor.execute(
        "SELECT STUDENT_ID FROM StudentsToClassrooms WHERE CLASSROOM_ID=?;", (class_id,)
    )
    rows3 = cursor.fetchall()
    if rows and not rows2:
        id = uuid.uuid4()
        cursor.execute(
            "INSERT INTO Assignments (ID, NAME, DESCRIPTION, CLASS_ID) VALUES (?,?,?,?)",
            (str(id), model.name, model.description, class_id),
        )
        for studentarr in rows3:
            student = studentarr[0]
            print(f"studentarr is {type(student)}")
            cursor.execute(
                "INSERT INTO SubmitAssignments (STUDENT_ID, ASSIGNMENT_ID, STATUS) VALUES (?,?,?)",
                (student, str(id), 0),
            )
        conn.commit()
        conn.close()
        return {
            "id": id,
            "title": model.name,
            "description": model.description,
            "class_id": class_id,
        }
    else:
        print(f"rows1 stats is {not not rows} and rows2 stats is {not rows2}")
        response.status_code = 400
        conn.close()


@app.put("/assignments/{assignment_id}", status_code=200)
def join_class(response: Response, model: models.AddAssignment, assignment_id):
    conn, cursor = start_db()
    cursor.execute(
        "SELECT * FROM Classrooms WHERE TEACHER_ID=? AND ID=?;",
        (model.teacher_id, model.class_id),
    )
    rows = cursor.fetchall()
    cursor.execute("SELECT * FROM Assignments WHERE ID=?;", (assignment_id,))
    rows2 = cursor.fetchall()
    print(f"Rows2 is receiving {not not rows2}")
    if rows and (not not rows2):
        id = uuid.uuid4()
        cursor.execute(
            "UPDATE Assignments SET NAME=?, DESCRIPTION=? WHERE ID=?",
            (model.name, model.description, assignment_id),
        )
        conn.commit()

        return {
            "id": assignment_id,
            "title": model.name,
            "description": model.description,
            "class_id": model.class_id,
        }
    else:
        print(f"rows1 stats is {not not rows} and rows2 stats is {not not rows2}")
        response.status_code = 400
        conn.close()


@app.delete("/assignments/{assignment_id}", status_code=204)
def register(response: Response, assignment_id):

    conn, cursor = start_db()
    cursor.execute("SELECT * FROM Assignments WHERE ID=?;", (assignment_id,))
    rows = cursor.fetchall()
    if rows:
        cursor.execute("DELETE FROM Assignments WHERE ID=?;", (assignment_id,))
        cursor.execute(
            "DELETE FROM SubmitAssignments WHERE ASSIGNMENT_ID=?;", (assignment_id,)
        )
        conn.commit()
        conn.close()
    else:
        response.status_code = 400
        conn.close()
        return


########### Submitting of an Assignment


@app.post("/submit/", status_code=200)
def login(model: models.SubmitAssignment, response: Response):
    conn, cursor = start_db()
    cursor.execute(
        "SELECT * FROM SubmitAssignments WHERE STUDENT_ID=? AND ASSIGNMENT_ID=?",
        (model.student_id, model.assignment_id),
    )
    rows = cursor.fetchall()
    print(rows)
    if rows:
        status = rows[0][2]
        new_status = 1 - status
        print(new_status)
        cursor.execute(
            "UPDATE SubmitAssignments SET STATUS=? WHERE STUDENT_ID=? AND ASSIGNMENT_ID=?;",
            (new_status, model.student_id, model.assignment_id),
        )
        conn.commit()
        return new_status
    conn.commit()


@app.post("/status/", status_code=200)
def status(model: models.SubmitAssignment, response: Response):
    conn, cursor = start_db()
    cursor.execute(
        "SELECT * FROM SubmitAssignments WHERE STUDENT_ID=? AND ASSIGNMENT_ID=?",
        (model.student_id, model.assignment_id),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


@app.post("/submissions/{class_id}", status_code=200)
def login(class_id, response: Response):
    conn, cursor = start_db()
    cursor.execute("SELECT * FROM Classrooms WHERE ID=?", (class_id,))
    rows1 = cursor.fetchall()
    if not rows1:
        conn.commit()
        return

    cursor.execute(
        "SELECT ID, NAME FROM StudentsToClassrooms JOIN Students ON StudentsToClassrooms.STUDENT_ID = Students.ID WHERE StudentsToClassrooms.CLASSROOM_ID=?;",
        (class_id,),
    )
    rows = cursor.fetchall()
    ids = [x[0] for x in rows]
    names = [x[1] for x in rows]  # Get list of Student ids and names

    output = dict()

    cursor.execute("SELECT ID,NAME FROM Assignments WHERE CLASS_ID=?", (class_id,))
    rows2 = cursor.fetchall()
    assignments = [x[0] for x in rows2]  # Get list of assignment IDs
    assignment_names = [x[1] for x in rows2]
    for (student_id, name) in zip(ids, names):
        student_report = dict()
        for (assignment, assignment_name) in zip(assignments, assignment_names):
            cursor.execute(
                "SELECT STATUS FROM SubmitAssignments WHERE STUDENT_ID=?AND ASSIGNMENT_ID=?",
                (student_id, assignment),
            )
            status = cursor.fetchall()
            student_report[assignment_name] = status
        output[name] = student_report
    conn.close()
    return [output, names, assignment_names]


# View Submission stats for a class
