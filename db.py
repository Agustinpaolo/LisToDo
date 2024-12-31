import sqlite3
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

def connect_db():
    return sqlite3.connect("tasks.db")

def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        status TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def load_user(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return User(id=user_data[0], username=user_data[1], password=user_data[2])
    return None

def load_user_by_username(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return User(id=user_data[0], username=user_data[1], password=user_data[2])
    return None

def get_tasks(filtro="todas", busqueda=""):
    conn = connect_db()
    cursor = conn.cursor()
    consulta = "SELECT id, task, status FROM tasks WHERE 1=1"
    parametros = []
    if filtro == "pendientes":
        consulta += " AND status = 'pendiente'"
    elif filtro == "completadas":
        consulta += " AND status = 'completada'"
    if busqueda:
        consulta += " AND task LIKE ?"
        parametros.append(f"%{busqueda}%")
    cursor.execute(consulta, parametros)
    tareas = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'pendiente'")
    pendientes = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'completada'")
    completadas = cursor.fetchone()[0]
    conn.close()
    return tareas, pendientes, completadas

def add_task(task):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task, status) VALUES (?, ?)", (task, "pendiente"))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def complete_task(task_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = 'completada' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def update_task(task_id, new_task):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET task = ? WHERE id = ?", (new_task, task_id))
    conn.commit()
    conn.close()
