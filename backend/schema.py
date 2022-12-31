import sqlite3

conn = sqlite3.connect("classroom.db")

conn.execute('DROP TABLE IF EXISTS Teachers;')
conn.execute('DROP TABLE IF EXISTS Assignments;')
conn.execute('DROP TABLE IF EXISTS Students;')
conn.execute('DROP TABLE IF EXISTS Classrooms;')
conn.execute('DROP TABLE IF EXISTS StudentsToClassrooms;')
conn.execute('DROP TABLE IF EXISTS SubmitAssignments;')

try:
    conn.execute('''CREATE TABLE Teachers
            (ID             TEXT UNIQUE NOT NULL,
            NAME           TEXT    NOT NULL,
            PASSWORD       TEXT    NOT NULL);
            ''')
except sqlite3.Error as er:
    print(' '.join(er.args))
    pass

try:
    conn.execute('''CREATE TABLE Students
            (ID  TEXT UNQUE NOT NULL,
            NAME           TEXT    NOT NULL,
            PASSWORD       TEXT    NOT NULL);
            ''')
except:
    print("Students couldn't successfully be created")
    pass

try:
    conn.execute('''CREATE TABLE StudentsToClassrooms
            (STUDENT_ID TEXT      NOT NULL,
            CLASSROOM_ID TEXT      NOT NULL);
            ''')
except:
    print("StudentsToClassrooms couldn't successfully be created")
    pass

try:
    conn.execute('''CREATE TABLE Classrooms
            (ID TEXT        UNIQUE NOT NULL,
            TITLE TEXT NOT NULL,
            DESCRIPTION           TEXT,
            TEACHER_ID        TEXT  NOT NULL,
            PRIMARY KEY (ID),
            FOREIGN KEY (ID) REFERENCES Users(ID));
            ''')
except:
    print("Classrooms couldn't successfully be created")
    pass

try:
    conn.execute('''CREATE TABLE Assignments
         (ID TEXT        UNIQUE NOT NULL,
         DESCRIPTION TEXT,
         NAME           TEXT    NOT NULL,
         CLASS_ID      TEXT  NOT NULL,
         FOREIGN KEY (ID) REFERENCES Classrooms(ID));
         ''')
except:
    print("Assignments couldn't successfully be created")
    pass


try:
    conn.execute('''CREATE TABLE SubmitAssignments
            (STUDENT_ID             TEXT NOT NULL,
            ASSIGNMENT_ID           TEXT    NOT NULL,
            STATUS       INT    NOT NULL);
            ''')
            
except sqlite3.Error as er:
    print(' '.join(er.args))
    pass

print("Successfully created/cleared database!")
