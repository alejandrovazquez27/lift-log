from flask import Flask, render_template, request, redirect, url_for

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
    "Calf Raises"
    "Ab crunches"
]
@app.route('/')
def home():
    return render_template('index.html')



@app.route('/push')
def push():
    return render_template('push.html', exercises=push_exercises)


@app.route("/push/exercises", methods=["POST"])
def add_push_exercise():
    exercise_name = request.form.get("exercise_name", "").strip()
    if exercise_name:
        push_exercises.append(exercise_name)
    return redirect(url_for("push"))


@app.route('/pull')
def pull():
    return render_template('pull.html', exercises=pull_exercises)

@app.route("/pull/exercises", methods=["POST"])
def add_pull_exercise():
    exercise_name = request.form.get("exercise_name", "").strip()
    if exercise_name:
        pull_exercises.append(exercise_name)
    return redirect(url_for("pull"))


@app.route('/legs')
def legs():
    return render_template('legs.html', exercises=leg_exercises)

@app.route('/legs/exercises', methods=["POST"])
def add_leg_exercise():
    exercise_name = request.form.get("exercise_name", "").strip()
    if exercise_name:
        leg_exercises.append(exercise_name)
    return redirect(url_for("legs"))
    

