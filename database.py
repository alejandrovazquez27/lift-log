import sqlite3

DATABASE = "workout.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
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

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()