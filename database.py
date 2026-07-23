import sqlite3

def initialize_database():
    connection = sqlite3.connect("slopeguard.db") #This links the python and database file
    cursor = connection.cursor() #This is what excutes

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        )
    """)
    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()