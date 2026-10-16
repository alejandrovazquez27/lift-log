from flask import Flask, render_template, request, redirect, url_for, abort
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
    
@app.route('/workouts/start/<split>', methods=['POST'])
def start_workout(split):
    valid_splits = ['push', 'pull', 'legs']
    
    if split not in valid_splits:
        abort(400)
    
    connection = get_connection()
    cursor = connection.execute(
    """
        INSERT INTO workout_sessions (split)
        VALUES (?)
    """,
        (split,)
    )
    session_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return redirect(url_for('view_workout', session_id=session_id))

@app.route("/workouts/<int:session_id>")
def view_workout(session_id):
    connection = get_connection()

    session = connection.execute(
        """
        SELECT * FROM workout_sessions
        WHERE id = ?
        """,
        (session_id,)
    ).fetchone()

    if session is None:
        connection.close()
        abort(404)

    exercises = connection.execute(
        """
        SELECT * FROM exercises
        WHERE split = ?
        ORDER BY name
        """,
        (session["split"],)
    ).fetchall()
    logged_sets = connection.execute(
    """
        SELECT ws.id, ws.set_number, ws.reps, ws.weight, e.name AS exercise_name
        FROM workout_sets ws
        JOIN exercises e ON ws.exercise_id = e.id
        WHERE ws.session_id = ?
        ORDER BY e.name,ws.set_number
    """,
    (session_id,)
).fetchall()
    connection.close()

    return render_template(
        "workout.html",
        session=session,
        exercises=exercises,
        logged_sets=logged_sets
    )
@app.route("/workouts/<int:session_id>/add_set", methods=["POST"])
def add_set(session_id):
    exercise_id = request.form.get("exercise_id")
    set_number = request.form.get("set_number")
    reps = request.form.get("reps")
    weight = request.form.get("weight")

    connection = get_connection()
    connection.execute(
        """
        INSERT INTO workout_sets (session_id, exercise_id, set_number, reps, weight)
        VALUES (?, ?, ?, ?, ?)
        """,
        (session_id, exercise_id, set_number, reps, weight)
    )
    connection.commit()
    connection.close()

    return redirect(url_for("view_workout", session_id=session_id))