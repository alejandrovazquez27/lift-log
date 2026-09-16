from flask import Flask, render_template

app = Flask(__name__)
push_exercies = [
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
    return render_template('push.html', exercises=push_exercies)
@app.route('/pull')
def pull():
    return render_template('pull.html', exercises=pull_exercises)
@app.route('/legs')
def legs():
    return render_template('legs.html', exercises=leg_exercises)

