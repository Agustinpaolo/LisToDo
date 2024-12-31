from flask import Flask, render_template, request, redirect, flash
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from db import init_db, get_tasks, add_task, delete_task, complete_task, update_task, load_user, load_user_by_username
import sqlite3

app = Flask(__name__)
app.secret_key = "t5709"

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(user_id):
    return load_user(user_id)

@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        nueva_tarea = request.form.get("task")
        if nueva_tarea:
            add_task(nueva_tarea)
            flash("Tarea creada exitosamente.", "success")
        else:
            flash("La tarea no puede estar vacía.", "danger")

    filtro = request.args.get("filtro", "todas")
    busqueda = request.args.get("busqueda", "")
    tareas, pendientes, completadas = get_tasks(filtro, busqueda)
    return render_template("index.html", tareas=tareas, pendientes=pendientes, completadas=completadas, filtro=filtro, busqueda=busqueda)

@app.route("/eliminar/<int:tarea_id>")
@login_required
def eliminar_tarea(tarea_id):
    delete_task(tarea_id)
    flash("Tarea eliminada exitosamente.", "success")
    return redirect("/")

@app.route("/completar/<int:tarea_id>")
@login_required
def completar_tarea(tarea_id):
    complete_task(tarea_id)
    flash("Tarea completada exitosamente.", "success")
    return redirect("/")

@app.route("/editar/<int:tarea_id>", methods=["GET", "POST"])
@login_required
def editar_tarea(tarea_id):
    if request.method == "POST":
        nuevo_texto = request.form.get("task")
        if nuevo_texto:
            update_task(tarea_id, nuevo_texto)
            flash("Tarea editada exitosamente.", "success")
        else:
            flash("El texto de la tarea no puede estar vacío.", "danger")
        return redirect("/")
    tarea = next((t for t in get_tasks()[0] if t[0] == tarea_id), None)
    return render_template("editar.html", tarea_id=tarea_id, tarea=tarea[1] if tarea else "")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"), method="pbkdf2:sha256", salt_length=8)

        try:
            conn = sqlite3.connect("tasks.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
        except sqlite3.IntegrityError:
            flash("El nombre de usuario ya existe", "danger")
        except sqlite3.Error as e:
            flash("Error al registrar el usuario.", "danger")
            print(f"Error de SQL: {e}")
        finally:
            conn.close()
        return redirect("/login")
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = load_user_by_username(username)
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Inicio de sesión exitoso.", "success")
            return redirect("/")
        else:
            flash("Usuario o contraseña incorrectos.", "danger")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión exitosamente.", "success")
    return redirect("/login")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
