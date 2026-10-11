from flask import Flask, render_template, request, redirect, url_for
from database import get_connection


app = Flask(__name__)
push_exercises = [
    "Bench Press",
    "Incline Dumbbell Press",
    "Shoulder Press",
    "Tricep Pushdowns"
]
pull_exercises = [
    "Barbell Rows",
    "Lat Pulldowns",
    "Rear Delt Flys",
    "Bicep Curls",
    "Hammer Curls"
]
leg_exercises = [
    "Leg Press",
    "Quad Extensions",
    "Hamstring Curls",
    "Calf Raises",
    "Ab crunches"
]
@app.route('/')
def home():
    return render_template('index.html')



@app.route('/push')
def push():
    connection = get_connection()
    exercises = connection.execute("SELECT * FROM exercises WHERE split = ? ORDER BY name", ("push",)).fetchall()
    connection.close()
    return render_template('push.html', exercises=exercises)


@app.route("/push/exercises", methods=["POST"])
def add_push_exercise():
    exercise_name = request.form.get("exercise_name", "").strip()
    if exercise_name:
        connection = get_connection()
        connection.execute(
            """
            INSERT OR IGNORE INTO exercises (name, split)
            VALUES (?, ?)
            """,
            (exercise_name, "push")
        )
        connection.commit()
        connection.close()
    return redirect(url_for("push"))


@app.route('/pull')
def pull():
    connection = get_connection()
    exercises = connection.execute("SELECT * FROM exercises WHERE split = ? ORDER BY name", ("pull",)).fetchall()
    connection.close()
    return render_template('pull.html', exercises=exercises)

@app.route("/pull/exercises", methods=["POST"])
def add_pull_exercise():
    exercise_name = request.form.get("exercise_name", "").strip()
    if exercise_name:
        connection = get_connection()
        connection.execute(
            """
            INSERT OR IGNORE INTO exercises (name, split)
            VALUES (?, ?)
            """,
            (exercise_name, "pull")
        )
        connection.commit()
        connection.close()
    return redirect(url_for("pull"))


@app.route('/legs')
def legs():
    connection = get_connection()
    exercises = connection.execute("SELECT * FROM exercises WHERE split = ? ORDER BY name", ("legs",)).fetchall()
    connection.close()
    return render_template('legs.html', exercises=exercises)

@app.route('/legs/exercises', methods=["POST"])
def add_leg_exercise():
    exercise_name = request.form.get("exercise_name", "").strip()
    if exercise_name:
        connection = get_connection()
        connection.execute(
            """
            INSERT OR IGNORE INTO exercises (name, split)
            VALUES (?, ?)
            """,
            (exercise_name, "legs")
        )
        connection.commit()
        connection.close()
    return redirect(url_for("legs"))
    

