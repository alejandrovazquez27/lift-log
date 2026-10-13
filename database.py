import sqlite3

DATABASE = "workout.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            split TEXT NOT NULL
                CHECK (split IN ('push', 'pull', 'legs')),
            UNIQUE (name, split)
        )
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS workout_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

        workout_date TEXT NOT NULL
            DEFAULT CURRENT_DATE,

        split TEXT NOT NULL
            CHECK (split IN ('push', 'pull', 'legs'))
       )
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS workout_sets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            exercise_id INTEGER NOT NULL,
            set_number INTEGER NOT NULL
                CHECK (set_number > 0),
            reps INTEGER NOT NULL
                CHECK (reps > 0),
            weight REAL NOT NULL
                CHECK (weight >= 0),
            FOREIGN KEY (session_id)
                REFERENCES workout_sessions(id)
                ON DELETE CASCADE,
            FOREIGN KEY (exercise_id)
                REFERENCES exercises(id)
                ON DELETE CASCADE,
            UNIQUE (session_id, exercise_id, set_number)
        )
    """)
    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()